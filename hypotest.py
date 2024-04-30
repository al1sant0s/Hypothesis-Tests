import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt

class hypotest:
    def __init__(self, sig, df, ts, cv, pvalue, alternative, reject, description):
        self.sig = sig                          # Significance level
        self.df = df                            # Degrees of freedom
        self.ts = ts                            # Test statistic
        self.cv = cv                            # Critical values
        self.pvalue = pvalue                    # Pvalue associated with the test
        self.alternative = alternative          # Type of alternative being used (left, right or bilateral).
        self.reject = reject                    # Boolean value that indicates if null hypothesis should be rejected or not given the results of the test.
        self.description = description          # A short description about the test


def t_test(data, mu_0, significance = 0.05, alternative = "bilateral"):

    n = data.size
    df = n - 1
    ts = (np.mean(data) - mu_0)/(np.sqrt(np.var(data, ddof = 1)/n))

    if(alternative == "bilateral"):
        cv = t.cdf((significance/2, 1 - significance/2), df = df)
        pvalue = 2 * t.cdf(-np.abs(ts), df = df)
    elif(alternative == "left"):
        cv = t.cdf(significance, df)
        pvalue = t.cdf(ts, df = df)
    else:
        cv = t.cdf(1 - significance, df = df)
        pvalue = 1 - t.cdf(ts, df = df)

    description = f"T {alternative} test for one population mean, with a significance level of {significance}, against {mu_0}."
    return hypotest(significance, df, ts, cv, pvalue, alternative, pvalue < significance,description)


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

test = t_test(data = dados, mu_0 = 5, alternative = "right")

print(test.ts, test.cv, test.pvalue, test.df)
