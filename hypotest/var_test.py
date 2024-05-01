import numpy as np
from scipy.stats import chi, f
import matplotlib.pyplot as plt
from hypotest import Hypotest

class HypoVarTest(Hypotest):
    def __init__(self, x, y = None, sigma_squared = 1, sig = 0.05, alternative = "bilateral"):
        if(y is not None):
            self.xvar = np.var(x, ddof = 1)
            self.yvar = np.var(x, ddof = 1)
            description = f"F {alternative} test for two population variances, with a significance level of {sig}, against {sigma_squared}."
            super().__init__(f(x.size - 1, y.size - 1), sig, np.array([x.size - 1, y.size - 1]), self.xvar/self.yvar, sigma_squared, alternative, description)
        else:
            self.xvar = np.var(x, ddof = 1)
            description = f"Chi-squared {alternative} test for one population variance, with a significance level of {sig}, against {sigma_squared}."
            super().__init__(chi(x.size - 1), sig, x.size - 1, (x.size - 1)*self.xvar/sigma_squared, sigma_squared, alternative, description)

    def error02comp(self, v1):
        if(self.alternative == "right"):
            qt = self.cv * self.v0/v1
            return self.rv.cdf(qt)
        elif(self.alternative == "left"):
            qt = self.cv * self.v0/v1
            return 1 - self.rv.cdf(qt)
        else:
            qt1 = self.cv[0] * self.v0/v1
            qt2 = self.cv[1] * self.v0/v1 
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)

