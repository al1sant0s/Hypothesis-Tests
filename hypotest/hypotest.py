import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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


    def summarize(self, show = True, minimal = False, retrieve = False, align="l", border_style = "DOUBLE_BORDER", **kwargs):
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
            return results


    def plot_test(self, show_values = True, show_pvalue = False, lw = 3, colors = {}):

        fig, ax = plt.subplots(layout="constrained")  # a figure with a single Axes

        xoffset = 0.001
        x = np.linspace(self.rv.ppf(xoffset), self.rv.ppf(1 - xoffset), int(1/xoffset))
        y = self.rv.pdf(x)

        #true_colors = {"pdf": "tab:pink", "ts": "blue", "cr": "red", "ncr": "gray", "pv": "cyan", "bl": "tab:purple"}
        true_colors = {"pdf": "black", "ts": "blue", "cr": "red", "pv": "purple", "bl": "black"}
        #true_colors = {"pdf": "purple", "ts": "orange", "cr": "red", "pv": "cyan", "bl": "black"}
        #true_colors = {"pdf": "purple", "ts": "green", "cr": "red", "pv": "pink", "bl": "black"}
        #true_colors = {"pdf": "blue", "ts": "green", "cr": "red", "pv": "yellow", "bl": "black"}
        true_colors.update(colors)

        show_cr = False

        # Show rejection region only if pvalue is smaller than significance
        if(not(show_pvalue) or self.pvalue < self.sig):
            show_cr = True
            if(self.alternative == "bilateral"):
                include = np.logical_or(x <= self.cv.min(), x >= self.cv.max())
                ax.fill_between(x, 0, y, where = include, color = true_colors["cr"], label = "Rejection region")
            elif(self.alternative == "left"):
                include = (x <= self.cv)
                ax.fill_between(x, 0, y, where = include, color = true_colors["cr"], label = "Rejection region")
            elif(self.alternative == "right"):
                include = (x >= self.cv)
                ax.fill_between(x, 0, y, where = include, color = true_colors["cr"], label = "Rejection region")

        if(show_pvalue):
            if(self.alternative == "bilateral"):
                include = self.rv.ppf([self.pvalue/2, 1 - self.pvalue/2])
                include = np.logical_or(x <= include.min(), x >= include.max())
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = "P-value")
            elif(self.alternative == "left"):
                include = (x <= self.ts)
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = "P-value")
            elif(self.alternative == "right"):
                include = (x >= self.ts)
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = "P-value")

                
        #Elaborate rest of the plot
        if(not(show_cr)):
            ax.vlines(self.cv, 0, self.rv.pdf(self.cv), color = true_colors["cr"], linewidth = lw, linestyle = "dashdot", label = "Critical values")

        ax.vlines(self.ts, 0, self.rv.pdf(self.ts), color = true_colors["ts"], linewidth = lw, linestyle = "dashed", label = f"Statistic test")
        ax.plot(x, y, linewidth = lw, linestyle="solid", color = true_colors["pdf"], label=f"Probability density function")
        ax.hlines(0, np.min(ax.get_xticks()), np.max(ax.get_xticks()), color = true_colors["bl"], linewidth = lw)
        ax.legend()

        ax.set_title(f"{self.description} " + rf"$(\alpha = {self.sig})$" + f"\n{self.distribution}")

        if(show_values):
            ax.xaxis.set_major_locator(ticker.FixedLocator(np.hstack([self.cv, self.ts])))

        ax.set_xlim(x.min(), x.max())
        plt.show()
