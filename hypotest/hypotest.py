import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt

class Hypotest:
    def __init__(self, rv, sig, df, ts, v0, alternative, description):
        self.sig = sig                          # Significance level
        self.df = df                            # Degrees of freedom
        self.rv = rv                            # A random variable associated with the test statistic distribution
        self.ts = ts                            # Test statistic
        self.v0 = v0                            # Parameter value under the null hypothesis
        self.alternative = alternative          # Type of alternative being used (left, right or bilateral).
        self.description = description          # A short description about the test

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
