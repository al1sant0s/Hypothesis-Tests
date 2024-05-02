import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t
from prettytable import PrettyTable

class Hypotest:
    def __init__(self, rv, sig, ts, v0, alternative, description):

        self.sig = sig                                          # Significance level
        self.rv = rv                                            # A random variable associated with the test statistic distribution
        self.ts = ts                                            # Test statistic
        self.v0 = v0                                            # Parameter value under the null hypothesis
        self.alternative = alternative                          # Type of alternative being used (left, right or bilateral).
        self.description = description                          # A short description about the test

        # Compute pvalue and critical values associated with the test
        if(alternative == "bilateral"):
            self.cv = rv.ppf((self.sig/2, 1 - self.sig/2))
            self.pvalue = rv.cdf(self.ts)
            self.pvalue = 2 * (1 - self.pvalue) if self.pvalue > 0.5 else 2 * self.pvalue
        elif(alternative == "left"):
            self.cv = rv.ppf(self.sig)
            self.pvalue = rv.cdf(self.ts)
        else:
            self.cv = rv.ppf(1 - self.sig)
            self.pvalue = 1 - rv.cdf(self.ts)

        # Boolean value that indicates if null hypothesis should be rejected or not given the results of the test.
        self.reject = self.pvalue < self.sig


    def power(self, beta):
        return 1 - self.error02comp(beta)


    def summarize(self, show = True, retrieve = False, **kwargs):
        table = PrettyTable(["Hypothesis test attributes", "Results"], **kwargs)
        table.add_row(["Description", self.description])
        table.add_row(["Parameters of distribution", self.rv.stats()])
        table.add_row(["Significance level", self.sig])
        table.add_row(["Pvalue", self.pvalue])
        table.add_row(["Statistic test", self.ts])
        table.add_row(["Critical values", self.cv])
        table.add_row(["Value under null hypothesis", self.v0])
        table.add_row(["Alternative Hypothesis", self.alternative])
        if(show):
            print(table)
        if(retrieve):
            # Return all these values in a list.
            return [self.description, self.rv.args, self.sig, self.pvalue, self.ts, self.cv, self.v0, self.alternative]
