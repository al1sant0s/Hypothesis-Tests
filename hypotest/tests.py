import numpy as np
from scipy.stats import norm, t, chi2, f
import matplotlib.pyplot as plt
from .hypotest import Hypotest

### Setup anything needed before initalizing objects.

# Help with test description.

tail = {"left": "left one-tailed", "right": "right one-tailed", "bilateral": "two-tailed"}

### Tests available

class HypoTstudTest(Hypotest):
    def __init__(self, x, y = None, mu_0 = 0, sig = 0.05, alternative = "bilateral", var_equal = False):

        x = np.array(x)
        self.xmean = np.mean(x)
        nx = x.size
        varx = np.var(x, ddof = 1)

        if(y is not None):
            y = np.array(y)
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
            sampling_estimates = {"X sampling mean": self.xmean, "Y sampling mean": self.ymean}
            super().__init__(t(df = df), f"T({df})", sig, (self.xmean - self.ymean - mu_0)/self.estdv, mu_0, alternative, description, sampling_estimates)

        else:
            self.estdv = np.sqrt(varx/x.size)
            df = nx - 1
            description = f"One sampling T {tail[alternative]} test."
            sampling_estimates = {"X sampling mean": self.xmean}
            super().__init__(t(df = df), f"T({df})", sig, (self.xmean - mu_0)/self.estdv, mu_0, alternative, description, sampling_estimates)


    def error02comp(self, v1):
        if(self.alternative == "right"):
            qt = self.cv[0] + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt)
        elif(self.alternative == "left"):
            qt = self.cv[0] + (self.v0 - v1)/self.estdv
            return 1 - self.rv.cdf(qt)
        else:
            qt1 = self.cv[0] + (self.v0 - v1)/self.estdv
            qt2 = self.cv[1] + (self.v0 - v1)/self.estdv
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)


class HypoVarTest(Hypotest):
    def __init__(self, x, y = None, sigma_sqr0 = 1, sig = 0.05, alternative = "bilateral"):

        x = np.array(x)
        self.varx = np.var(x, ddof = 1)
        nx = x.size

        if(y is not None):
            y = np.array(y)
            self.vary = np.var(y, ddof = 1)
            ny = y.size
            description = f"F {tail[alternative]} test for two variances."
            sampling_estimates = {"X sampling variance": self.varx, "Y sampling variance": self.vary}
            super().__init__(f(dfn = nx - 1, dfd = ny - 1), f"F({nx - 1}, {ny - 1})", sig, self.varx/self.vary, sigma_sqr0,
                             alternative, description, sampling_estimates)
        else:
            description = f"Chi-squared {tail[alternative]} test for variance."
            sampling_estimates = {"X sampling variance": self.varx}
            super().__init__(chi2(df = nx - 1), f"Chi-Squared({nx - 1})", sig, (nx - 1)*self.varx/sigma_sqr0, sigma_sqr0,
                             alternative, description, sampling_estimates)


    def error02comp(self, v1):
        if(self.alternative == "right"):
            qt = self.cv[0] * self.v0/v1
            return self.rv.cdf(qt)
        elif(self.alternative == "left"):
            qt = self.cv[0] * self.v0/v1
            return 1 - self.rv.cdf(qt)
        else:
            qt1 = self.cv[0] * self.v0/v1
            qt2 = self.cv[1] * self.v0/v1 
            return self.rv.cdf(qt2) - self.rv.cdf(qt1)

class HypoPropTest(Hypotest):
    def __init__(self, p1, n1, p2 = None, n2 = None, pi0 = 0, sig = 0.05, alternative = "bilateral"):
        self.prop1 = p1
        self.n1 = n1
        if(p2 is not None and n2 is not None):
            self.prop2 = p2
            self.n2 = n2
            self.estdv = np.sqrt(p1*(1 - p1)/n1 + p2*(1 - p2)/n2)
            description = f"Z {tail[alternative]} test for two proportions."
            sampling_estimates = {"Sampling proportion 01": self.prop1, "Sampling proportion 02": self.prop2,
                                  "Sampling size 01": self.n1, "Sampling size 02": self.n2}
            super().__init__(norm(), f"Normal(0, 1)", sig, ((p1 - p2) - pi0)/self.estdv, pi0, alternative, description, sampling_estimates)
        else:
            self.estdv = np.sqrt(pi0*(1 - pi0)/n1) 
            description = f"Z {tail[alternative]} test for one proportion."
            sampling_estimates = {"Sampling proportion": self.prop1, "Sampling size": self.n1}
            super().__init__(norm(), f"Normal(0, 1)", sig, (p1 - pi0)/self.estdv, pi0, alternative, description, sampling_estimates)
    def error02comp(self, v1):
        return HypoTstudTest.error02comp(self, v1)
