import numpy as np
from scipy.stats import norm, t, chi2, f
from scipy.stats import chi2, f
import matplotlib.pyplot as plt
from .hypotest import Hypotest

### Setup anything needed before initalizing objects.

# Help with test description.

tail = {"left": "left one-tailed", "right": "right one-tailed", "bilateral": "two-tailed"}


### Tests available

class HypoTstudTest(Hypotest):
    def __init__(self, x, y = None, mu_0 = 0, sig = 0.05, alternative = "bilateral", var_equal = False):

        self.xmean = np.mean(x)
        nx = x.size
        varx = np.var(x, ddof = 1)

        if(y is not None):
            self.ymean = np.mean(y)
            ny = y.size
            vary = np.var(y, ddof = 1)

            if(var_equal):
                # Uses pooled standard deviation
                self.estdv = np.sqrt((1/nx + 1/ny) * (varx * (nx - 1) + vary * (ny - 1))/((nx - 1) + (ny - 1)))
                df = (nx - 1) + (ny - 1)
            else:
                self.estdv = np.sqrt(varx/nx + vary/ny)

                # Estimates degrees of freedom using (Satterthwaite Adjustment):
                rx = varx/nx
                ry = vary/ny
                df = ((rx + ry)**2)/((rx**2)/(nx - 1) + (ry**2)/(ny - 1))

            description = f"Two sampling T {tail[alternative]} test."
            super().__init__(t(df = df), sig, (self.xmean - self.ymean - mu_0)/self.estdv, mu_0, alternative, description)

        else:
            self.estdv = np.sqrt(np.var(x, ddof = 1)/x.size)
            description = f"One sampling T {tail[alternative]} test."
            df = nx - 1
            super().__init__(t(df), sig, (self.xmean - mu_0)/self.estdv, mu_0, alternative, description)


    def error02comp(self, v1):
        if(self.alternative == "right"):
            qt = self.cv + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt)
        elif(self.alternative == "left"):
            qt = self.cv + (self.v0 - v1)/self.estdv
            return 1 - self.rv.cdf(qt)
        else:
            qt1 = self.cv[0] + (self.v0 - v1)/self.estdv
            qt2 = self.cv[1] + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)


class HypoVarTest(Hypotest):
    def __init__(self, x, y = None, sigma_squared = 1, sig = 0.05, alternative = "bilateral"):

        self.varx = np.var(x, ddof = 1)
        nx = x.size

        if(y is not None):
            self.vary = np.var(y, ddof = 1)
            ny = y.size
            description = f"F {tail[alternative]} test for two variances."
            super().__init__(f(dfn = nx - 1, dfd = ny - 1), sig, self.varx/self.vary, sigma_squared, alternative, description)
        else:
            description = f"Chi-squared {tail[alternative]} test for variance."
            super().__init__(chi2(df = nx - 1), sig, (nx - 1)*self.varx/sigma_squared, sigma_squared, alternative, description)


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


class HypoPropTest(Hypotest):
    def __init__(self, P, n, pi, sig = 0.05, alternative = "bilateral"):
        self.prop = P
        self.n = n
        self.estdv = np.sqrt((P - pi)/n) 
        description = f"Z {tail[alternative]} test for one proportion."
        super().__init__(norm(), sig, (P - pi)/self.estdv, pi, alternative, description)

    def error02comp(self, v1):
        if(self.alternative == "right"):
            qt = self.cv + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt)
        elif(self.alternative == "left"):
            qt = self.cv + (self.v0 - v1)/self.estdv
            return 1 - self.rv.cdf(qt)
        else:
            qt1 = self.cv[0] + (self.v0 - v1)/self.estdv
            qt2 = self.cv[1] + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)
