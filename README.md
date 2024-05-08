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

Before using this package, you need to make sure to have installed numpy, scipy, matplotlib and prettytable onto your system.
You can install them pasting the following command `pip install numpy scipy matplotlib prettytable` into your cli.

After installation of said requirements, you can install this package following these steps:

1. Inside your terminal, get into the root of your project directory.
2. Use the following command to download the package `git clone https://github.com/al1sant0s/Hypothesis-Tests/`
3. Finally, import the package from your main python file adding this to line `import hypotest`.
