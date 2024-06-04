import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import prettytable

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
            self.cv = np.array([rv.ppf(self.sig)])
            self.pvalue = rv.cdf(self.ts)
        else:
            self.cv = np.array([rv.ppf(1 - self.sig)])
            self.pvalue = 1 - rv.cdf(self.ts)

        # Boolean value that indicates if null hypothesis should be rejected or not given the results of the test.
        self.reject = self.pvalue < self.sig


    def power(self, v1, show = True, align="l", border_style = "DOUBLE_BORDER", **kwargs):

        v1 = np.array(v1)

        table = prettytable.PrettyTable(["Values under alternative hypothesis", "Type II error (Beta)", "Power (1 - Beta)"], **kwargs)
        table.hrules = prettytable.ALL

        # Set border style
        table.set_style(getattr(prettytable, border_style))

        powers = np.array([])

        for i in v1:
            err2 = self.error02comp(i)
            table.add_row([i, err2, 1 - err2])
            powers = np.concatenate([powers, [1 - err2]])
        table.align = align

        if(show):
            print(table)

        # Return everything in a numpy array.
        return powers


    def summarize(self, show = True, minimal = False, align="l", border_style = "DOUBLE_BORDER", **kwargs):
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

        results = np.array([self.description, self.distribution, self.v0, self.alternative, self.sig, self.pvalue, self.reject])
        if(not(minimal)):
            table.add_rows([[key, self.sampling_estimates[key]] for key in self.sampling_estimates])
            table.add_row(["Statistic test", self.ts])
            table.add_row(["Critical values", self.cv])
            results = np.concatenate([results, list(self.sampling_estimates.values()), [self.ts], self.cv])

        if(show):
            print(table)

        # Return everything in a numpy array.
        return results


    def plot_test(self, show_values = True, fill_pvalue = False, lw = 2, colors = {}):

        fig, ax = plt.subplots(layout="constrained")  # a figure with a single Axes

        xoffset = 0.001
        x = np.linspace(self.rv.ppf(xoffset), self.rv.ppf(1 - xoffset), int(1/xoffset))
        y = self.rv.pdf(x)

        true_colors = {"pdf": "#8c8c8c", "ts": "#D2B48C", "cr": "#F08080", "pv": "#FFE4C4", "bl": "#696969"}
        true_colors.update(colors)

        show_cr = False

        # Show rejection region only if pvalue is smaller than significance
        if(not(fill_pvalue) or self.pvalue < self.sig):
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

        if(fill_pvalue):
            if(self.alternative == "bilateral"):
                include = self.rv.ppf([self.pvalue/2, 1 - self.pvalue/2])
                include = np.logical_or(x <= include.min(), x >= include.max())
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = f"P-value")
            elif(self.alternative == "left"):
                include = (x <= self.ts)
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = f"P-value")
            elif(self.alternative == "right"):
                include = (x >= self.ts)
                ax.fill_between(x, 0, y, where = include, color = true_colors["pv"], label = f"P-value")

                
        #Elaborate rest of the plot
        if(not(show_cr)):
            ax.vlines(self.cv, 0, self.rv.pdf(self.cv), color = true_colors["cr"], linewidth = lw, linestyle = "dashdot", label = "Critical values")

        ax.vlines(self.ts, 0, self.rv.pdf(self.ts), color = true_colors["ts"], linewidth = lw, linestyle = "dashed", label = f"Statistic test")
        ax.plot(x, y, linewidth = lw, linestyle="solid", color = true_colors["pdf"], label=f"Probability density function")
        ax.hlines(0, np.min(ax.get_xticks()), np.max(ax.get_xticks()), color = true_colors["bl"], linewidth = lw)
        ax.legend()

        ax.set_title(f"{self.description} " + rf"$(\alpha = {self.sig})$" + f"\n{self.distribution}")

        # Show values of the test in the plot or display a generic x axis.
        if(show_values):
            ax.xaxis.set_major_locator(ticker.FixedLocator(self.cv))
            crop_distance = np.min(np.array([self.ts - x.min(), x.max() - self.ts]))
            crop_offset = 0.2
            if(crop_distance > crop_offset * (x.max() - x.min())):
                if(self.alternative == "left"):
                    ax.text(self.ts, self.rv.pdf(self.ts)/2, f"{self.ts:.4f}", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                            rotation = "vertical", horizontalalignment = "right", verticalalignment = "center", fontsize = "large", fontstyle = "italic")
                    if(fill_pvalue):
                        xpos = self.ts - crop_offset * crop_distance
                        ypos = np.min(self.rv.pdf(np.array([self.ts, xpos])))/2
                        ax.text(xpos, ypos, f"{(self.pvalue*100):.2f}%", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                                rotation = "horizontal", horizontalalignment = "center", verticalalignment = "bottom", fontsize = "large", fontstyle = "italic")
                elif(self.alternative == "right"):
                    ax.text(self.ts, self.rv.pdf(self.ts)/2, f"{self.ts:.4f}", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                            rotation = "vertical", horizontalalignment = "right", verticalalignment = "center", fontsize = "large", fontstyle = "italic")
                    if(fill_pvalue):
                        xpos = self.ts + crop_offset * crop_distance
                        ypos = np.min(self.rv.pdf(np.array([self.ts, xpos])))/2
                        ax.text(xpos, ypos, f"{(self.pvalue*100):.2f}%", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                                rotation = "horizontal", horizontalalignment = "center", verticalalignment = "bottom", fontsize = "large", fontstyle = "italic")
                else:
                    ax.text(self.ts, self.rv.pdf(self.ts)/2, f"{self.ts:.4f}", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                            rotation = "vertical", horizontalalignment = "right", verticalalignment = "center", fontsize = "large", fontstyle = "italic")
                    if(fill_pvalue):
                        xrange = self.rv.ppf([self.pvalue/2, 1 - self.pvalue/2])
                        xpos = np.min(xrange) - crop_offset * crop_distance
                        ypos = np.min(self.rv.pdf(xpos))/2
                        ax.text(xpos, ypos, f"{(self.pvalue*50):.2f}%", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                                rotation = "horizontal", horizontalalignment = "center", verticalalignment = "bottom", fontsize = "large", fontstyle = "italic")
                        xpos = np.max(xrange) + crop_offset * crop_distance
                        ypos = np.min(self.rv.pdf(xpos))/2
                        ax.text(xpos, ypos, f"{(self.pvalue*50):.2f}%", alpha = 0.5, backgroundcolor = "#ff000000", color = "black",
                                rotation = "horizontal", horizontalalignment = "center", verticalalignment = "bottom", fontsize = "large", fontstyle = "italic")
            else:
                ax.xaxis.set_major_locator(ticker.AutoLocator())


        ax.set_xlim(x.min(), x.max())
        plt.show()


    def plot_power(self, v1, lw = 2, color = "#4682B4"):

        fig, ax = plt.subplots(layout="constrained")  # a figure with a single Axes

        x = np.array(v1)
        y = self.power(v1, show = False)

        ax.plot(x, y, linewidth = lw, linestyle="solid", color = color)

        ax.set_xlabel(r"Values under $\mathscr{H}_1$")  # Add an x-label to the axes.
        ax.set_ylabel(r'$1 - \beta$')  # Add a y-label to the axes.

        ax.set_title(f"Power curve for {self.description}")

        plt.show()
