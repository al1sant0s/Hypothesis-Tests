import numpy as np
import matplotlib.pyplot as plt
import prettytable
from scipy.stats import norm, t

class Hypotest:
    def __init__(self, rv, distribution, sig, ts, v0, alternative, description, sampling_estimates = {}):

        self.sig = sig                                          # Significance level
        self.rv = rv                                            # A random variable associated with the test statistic distribution
        self.distribution = distribution                        # The distribution used in the test
        self.ts = ts                                            # Test statistic
        self.v0 = v0                                            # Parameter value under the null hypothesis
        self.alternative = alternative                          # Type of alternative being used (left, right or bilateral).
        self.description = description                          # A short description about the test
        self.sampling_estimates = sampling_estimates            # This will be a dictonary with the specific statistic values for the test

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


    def summarize(self, show = True, minimal = True, retrieve = False, align="l", border_style = "DOUBLE_BORDER", **kwargs):
        table = prettytable.PrettyTable(["Hypothesis test attributes", "Results"], **kwargs)

        # Set border style
        table.set_style(getattr(prettytable, border_style))

        table.align = align
        table.add_row(["Description", self.description])
        table.add_row(["Distribution utilized", self.distribution])
        table.add_row(["Value under null hypothesis", self.v0])
        table.add_row(["Alternative Hypothesis", self.alternative])
        table.add_row(["Significance level", self.sig])
        table.add_row(["Pvalue", self.pvalue])
        table.add_row(["Rejet null hypothesis?", "Yes" if self.reject else "No"])

        results = [self.description, self.distribution, self.v0, self.alternative, self.sig, self.pvalue, self.reject]
        if(not(minimal)):
            table.add_rows([[key, self.sampling_estimates[key]] for key in self.sampling_estimates])
            table.add_row(["Statistic test", self.ts])
            table.add_row(["Critical values", self.cv])
            results = results + list(self.sampling_estimates.values()) + [self.ts, self.cv]

        if(show):
            print(table)

        if(retrieve):
            # Return everything in a list.
            return print(results)
