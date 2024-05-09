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

Before getting into practical usage of the tests, some clarification about some small technical details needs to be done.
Each test is built from a specific class. Bellow are listed the classes used to perform each test:

* `HypoTstudTest` class performs tests for mean(s) using one or two samples.
* `HypoVarTest` class performs tests for variance(s) using one or two samples.
* `HypoPropTest` class performs tests for one proportion.
* `HypoProp02Test` class performs tests for two proportions.

Also there is one special class called Hypotest. `Hypotest` class does not perform any test.
It just serves as the base class used to construct the classes above. **You will never need to interact directly with this class.**

To perform a test, call one of the 4 classes mentioned before and pass the arguments needed for them. An object of `Hypotest` class will be returned.
This object will have many attributes and methods. Bellow are listed **only** the most important attributes and methods that might be useful:

* Attributes available for all tests objects:
   * sig: significance level of the test.
   * ts: test statistic value of the test.
   * v0: test value under null hypothesis.
   * alternative: type of alternative hypothesis being used (left, right or bilateral).
   * description: a short description about the test.
   * sampling_estimates: this will be a dictonary with specific statistic values for the test.
   * cv: a numpy array with one or two critical values of the test.
   * pvalue: self-explanatory.
   * reject: a boolean variable that tells if null hypothesis should be rejected (or not).

* Methods available:
   * `power(self, v1, show = True, align = 'l', border_style = "DOUBLE_BORDER", **kwargs)`
     computes power of test for values passed through v1 parameter. Each argument is explained bellow.
     * v1: a single or sequence of values for power to be computed from.
     * show: if set to True, it will print a table built from Prettytable with results.
     * align: this parameter is from `Prettytable` class and it determines the alignment of the table. You can use 'l' for left, 'c' for centered and 'r' for right alignment.
     * border_style: this parameter is from `Prettytable` class and it determines the border style of the table.
     * **kwargs: additional keywords for `Prettytable`. You can learn more about prettytable [here](https://pypi.org/project/prettytable/).
     It returns a numpy array with the powers calculated for each v1 value.

these general
attributes and methods that are available for all classes
