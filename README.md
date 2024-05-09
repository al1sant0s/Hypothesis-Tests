# Hypothesis-Tests


## About

Inspired by R functions: t.test, var.test and prop.test; this python package allows you to perform some basic hypothesis tests. Right now there are 6 types of
tests available, they are:

* One sample tests
    * T-student test for true value of mean.
    * Chi-squared test for true value of variance.
    * Z test for true value of proportion.
* Two sample tests
    * T-student test for the difference between two means.
    * F test for the ratio between two variances.
    * Z test for the difference between two proportions.

More tests might be added in the future.

## Installation

Before using this package, you need to make sure to have installed numpy, scipy, matplotlib and prettytable into your system.
You can install them pasting the following command `pip install numpy scipy matplotlib prettytable` into your terminal shell.

After installation of aforementioned requirements, you can install this package following these steps:

1. Inside your terminal, get into the root of your project directory. Normally, you do this with cd command.
2. Use the following command to download the package `git clone https://github.com/al1sant0s/Hypothesis-Tests/ Hypothesis`
3. Finally, import the package to your main python file adding this line `import Hypothesis.hypotest as hypotest` somewhere at the beggining of the file.

Now you are ready to start.

## How it works?

Before getting into practical usage of the tests, some clarification needs to be done.
If you wish, you can skip straight to the usage section and come back here later in case you need more details.

Each test is built from a specific class. Bellow are listed the classes used to perform each test:

* `HypoTstudTest` class performs tests for mean(s) using one or two samples.
* `HypoVarTest` class performs tests for variance(s) using one or two samples.
* `HypoPropTest` class performs tests for one proportion.
* `HypoProp02Test` class performs tests for two proportions.

Also there is one special class called Hypotest. `Hypotest` class does not perform any test.
It just serves as the base class used to construct the classes above. **You will never need to interact directly with this class.**

To perform a test, call one of the 4 classes mentioned before and pass the arguments needed for them. The parameters you need to pass
to them are described bellow.

### `HypoTstudTest(self, x, y = None, mu_0 = 0, sig = 0.05, alternative = "bilateral", var_equal = False)`
Used to perform tests for mean(s) using one or two samples.
   * x: the first sample for the test. It can be a list of a numpy array.
   * y (optional): The second sample for the test. It can be a list of a numpy array.
   * mu_0: this represents the value under null hypothesis. For one sample tests this is the true mean. For two samples tests
     this is the difference between the means.
   * sig: the significance level used for this test.
   * alternative: determines the direction of the test. The values available are the following: "left", "right", "bilateral".
   * var_equal (only used for two samples tests): indicates whether the two samples are taken from two populations with the same variance.

### `HypoVarTest(self, x, y = None, sigma_sqr0 = 1, sig = 0.05, alternative = "bilateral")`
Used to perform tests for variance(s) using one or two samples.
   * x: the first sample for the test. It can be a list of a numpy array.
   * y (optional): The second sample for the test. It can be a list of a numpy array.
   * sigma_sqr0: this represents the value under null hypothesis. For one sample tests this is the true variance. For two samples tests
     this is the ratio between the variances.
   * sig: the significance level used for this test.
   * alternative: determines the direction of the test. The values available are the following: "left", "right", "bilateral".

### `HypoPropTest(self, P, n, pi0, sig = 0.05, alternative = "bilateral")`
Used to perform tests for one proportion.
   * P: the sample proportion.
   * n: the size of the sample which the P proportion was taken from.
   * pi0: this represents the value under null hypothesis. The true value of the proportion in the population.
   * sig: the significance level used for this test.
   * alternative: determines the direction of the test. The values available are the following: "left", "right", "bilateral".
    
### `HypoProp02Test(self, p1, p2, n1, n2, pi0 = 0, sig = 0.05, alternative = "bilateral")`
Used to perform tests for two proportions.
   * p1: the sample 01 proportion.
   * p2: the sample 02 proportion.
   * n1: the size of the sample 01 which the p1 proportion was taken from.
   * n2: the size of the sample 02 which the p1 proportion was taken from.
   * pi0: this represents the value under null hypothesis. The value of the difference between the two proportions in the populations.
   * sig: the significance level used for this test.
   * alternative: determines the direction of the test. The values available are the following: "left", "right", "bilateral".

For any of these, an object of `Hypotest` class will be returned.
This object will have many attributes and methods. Bellow are listed **only** the most important attributes and methods that might be useful:

* Attributes available for all test objects:
   * sig: significance level of the test.
   * ts: test statistic value of the test.
   * v0: test value under null hypothesis.
   * alternative: type of alternative hypothesis being used (left, right or bilateral).
   * description: a short description about the test.
   * sampling_estimates: this will be a dictonary with specific statistic values for the test.
   * cv: a numpy array with one or two critical values of the test.
   * pvalue: self-explanatory.
   * reject: a boolean variable that tells if null hypothesis should be rejected (or not).

* Methods available for all test objects:
   * `power(self, v1, show = True, align = 'l', border_style = "DOUBLE_BORDER", **kwargs)`
     computes power of test for values passed through v1 parameter.
     * v1: a single or sequence of values for power to be computed from. These are all values under alternative hypothesis.
     * show: if set to True, it will print a table built from prettytable with results.
     * align: this parameter is from `Prettytable` class and it determines the alignment of the table. You can use 'l' for left, 'c' for centered and 'r' for right alignment.
     * border_style: this parameter is from `Prettytable` class and it determines the border style of the table. Any border style supported from prettytable can be passed as a string.
     * **kwargs: additional keywords for `Prettytable`. You can learn more about prettytable [here](https://pypi.org/project/prettytable/).
     
     It returns a numpy array with the powers calculated for each v1 value.

  * `summarize(self, show = True, minimal = False, align = "l", border_style = "DOUBLE_BORDER", **kwargs)` assembles information from the test.
     * show: if set to True, it will print a table built from prettytable with results.
     * minimal: if set to True, it will print less information, otherwise it will print all info available for the test.
       Set this parameter to true if you wish to have different kinds of tests with same standard tables.
     * align: this parameter is from `Prettytable` class and it determines the alignment of the table. You can use 'l' for left, 'c' for centered and 'r' for right alignment.
     * border_style: this parameter is from `Prettytable` class and it determines the border style of the table. Any border style supported from prettytable can be passed as a string.
     * **kwargs: additional keywords for `Prettytable`. You can learn more about prettytable [here](https://pypi.org/project/prettytable/).
   
    It returns a numpy array with the results presented in table in the order they appear (from top to bottom).

  * `plot_test(self, show_values = True, show_pvalue = False, lw = 3, colors = {})` will make a plot of the test itself.
     * show_values: if set to True, it will show critical values and the test statistic value on x axis, otherwise it will let matplotlib choose the x axis marks (ticks).
     * show_pvalue: if set to True, it will fill the area associated with the pvalue of the test.
     * lw: control the linewidth of the lines of the plot.
     * colors: this dictonary is used to plot the test with different colors than default. Bellow are the keys you can put in this dictonary along with the default colors used.
       * `"pdf": "black` color of the probability density function (curve).
       * `"ts": "blue"` color of the dashed line that indicates the test statistic position.
       * `"cr": "red"` color of the critical region.
       * `"pv": "purple"` color used to fill pvalue area.
       * `"bl": "black"` color of the bottom line.
       
       You can use any color supported by matplotlib. For more details, check [this](https://matplotlib.org/stable/users/explain/colors/colors.html).
       The keys that you pass will update the colors of the associated components. This means that you don't need to pass all of them, but only the ones you wish to change.
       
   * `plot_power(self, v1, lw = 3)` will make a plot of the power (power curve) for each value passed through v1.
     * v1: a single or sequence of values for power to be computed from. These are all values under alternative hypothesis.
      * lw: control the linewidth of the lines of the plot.

With all of this out of the way, now let's jump into action with some examples of usage.

## Usage

### Summarize test

### Visualizing test

these general
attributes and methods that are available for all classes
