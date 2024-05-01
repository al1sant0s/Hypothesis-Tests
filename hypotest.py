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

class TestT(Hypotest):
    def __init__(self, x, y = None, mu_0 = 0, sig = 0.05, alternative = "bilateral"):
        if(y != None):
            pass
        else:
            self.xmean = np.mean(x)
            self.estdv = np.sqrt(np.var(x, ddof = 1)/x.size)
            description = f"T {alternative} test for one population mean, with a significance level of {sig}, against {mu_0}."
        super().__init__(t(x.size - 1), sig, x.size - 1, (self.xmean - mu_0)/self.estdv, mu_0, alternative, description)

    def error02comp(self, v1):
        if(self.alternative == "bilateral"):
            qt1 = self.cv[0] + (self.v0 - v1)/self.estdv
            qt2 = self.cv[1] + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)


dados = np.array([
13.6914485,   0.2957456,   3.7377565,   6.9602491,  15.2862238,   5.4180188,
 3.3530132,   0.7743940,  -0.3085460,   9.6825667,   0.7898673,  -1.1426805,
13.9555585,   6.5996481,   3.3264209,  14.5456466,   4.9335114,   5.4967958,
10.3396785,   0.7583997, -10.1072548,  14.0997402,  19.1044744,   2.4582297,
 3.9788961,   0.3269203,   6.1639448,  11.4197698,   4.1903689,   5.7964073,
 4.8945119,   9.3564881,   5.9304306,   0.7929093,   1.8100409,   0.1795812,
 7.1847321,  14.2355209,   7.5799259,   4.6734115,   7.1796968,  -3.8983067,
15.6965885,  20.0378430,  17.1616795,  12.8491778,  -3.6045550,  -2.7168218,
 5.0238398,   8.7786545])

test = TestT(x = dados, mu_0 = 5, sig = 0.05)

print(test.ts, test.cv, test.pvalue, test.df, test.error02comp(6))
