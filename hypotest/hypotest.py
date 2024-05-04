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


    def plot_test(self, fill_pvalue = True, fill_rejection = True, fill_nonrejection = False, lw = 3, colors = {}):

        fig, ax = plt.subplots(layout="constrained")  # a figure with a single Axes

        xoffset = 0.001

        x = np.linspace(self.rv.ppf(xoffset), self.rv.ppf(1 - xoffset), int(1/xoffset))
        y = self.rv.pdf(x)

        #true_colors = {"pdf": "tab:pink", "ts": "blue", "cr": "red", "ncr": "gray", "pv": "cyan", "bl": "tab:purple"}
        true_colors = {"pdf": "purple", "ts": "orange", "cr": "red", "ncr": "gray", "pv": "cyan", "bl": "black"}
        true_colors.update(colors)

        ax.plot(x, y, linewidth = lw, linestyle="solid", color = true_colors["pdf"], alpha = 1, label=f"Probability density function")
        ax.hlines(0, np.min(ax.get_xticks()), np.max(ax.get_xticks()), color = true_colors["bl"])
        ax.vlines(self.cv, 0, self.rv.pdf(self.cv), color = true_colors["cr"], linewidth = lw, linestyle = "solid", label = f"Rejection values")
        ax.vlines(self.ts, 0, self.rv.pdf(self.ts), color = true_colors["ts"], linewidth = lw, linestyle = "dashed", label = f"Statistic test")

        ax.set_title(self.description)
        #ax.xaxis.set_major_locator(ticker.MultipleLocator(base = 0.5, offset = 0))
        ax.set_xlim(x.min(), x.max())
        ax.text(75, .025, r"$\mu=115,\ \sigma=15$")

        if(fill_pvalue):

            if(self.alternative == "bilateral"):
                exclude = self.rv.ppf([self.pvalue/2, 1 - self.pvalue/2])
                ax.fill_between(x, 0, y, where = np.logical_or(x <= exclude.min(), x >= exclude.max()))
            else:
                if(self.alternative == "left"):
                    include = (x <= self.ts).sum() - 1
                    ax.fill_between(x[0:include], 0, y[0:include])
                elif(self.alternative == "right"):
                    exclude = (x <= self.ts).sum()
                    ax.fill_between(x[exclude:], 0, y[exclude:])
                
            ax.legend()

        else:
            pass

        
        #ax.set_xticks(list(ax.get_xticks()) + [self.pvalue], [str(a) for a in ax.get_xticks()] + ["pvalue"])
        plt.show()
