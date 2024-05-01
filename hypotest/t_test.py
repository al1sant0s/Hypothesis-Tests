import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt
from hypotest import Hypotest

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

            description = f"T {alternative} test for two a difference in two population means, with a significance level of {sig}, against {mu_0}."
            super().__init__(t(df), sig, df, (self.xmean - self.ymean - mu_0)/self.estdv, mu_0, alternative, description)

        else:
            self.estdv = np.sqrt(np.var(x, ddof = 1)/x.size)
            description = f"T {alternative} test for one population mean, with a significance level of {sig}, against {mu_0}."
            df = nx - 1
            super().__init__(t(df), sig, df, (self.xmean - mu_0)/self.estdv, mu_0, alternative, description)

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

