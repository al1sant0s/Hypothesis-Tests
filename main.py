import numpy as np
import hypotest as hypotest

rng = np.random.default_rng(1)
sample01 = rng.normal(5, 6, 25)
sample02 = rng.normal(4.6, 6, 25)

one_mean_test = hypotest.HypoTstudTest(x = sample01, mu_0 = 5, sig = 0.05, alternative = "bilateral")

print("\n--- Test for one mean done! Results presented bellow. ---\n")
one_mean_test.summarize() # See the results

print("\n--- Print the same table with less information and with a different appearance. ---\n")
one_mean_test.summarize(minimal = True, border_style = "SINGLE_BORDER") # See the results

results = one_mean_test.summarize(show = False, minimal = True, border_style = "SINGLE_BORDER") # Get the results

# Check pvalue using both the class attribute and the results (the 6th line of the table is where pvalue appear so we use 5 as index).
print(one_mean_test.pvalue, results[5]) # it should print the same value twice

# Print everything from results.
print(results)

one_mean_test.plot_test() # visualize test

# We use var_equal = True because we know the samples were taken from 2 populations with same variance.
two_mean_test = hypotest.HypoTstudTest(x = sample01, y = sample02, mu_0 = 0, sig = 0.07, alternative = "left", var_equal = True)

print("\n--- Test for two means done! Results presented bellow. ---\n")
two_mean_test.summarize() # See the results

two_mean_test.plot_test() # plot the test without showing pvalue area
two_mean_test.plot_test(fill_pvalue = True, lw = 5) # now plot the test showing pvalue area

two_mean_test.plot_power(np.linspace(-10,2,100), lw = 5) # plot power curve with a thicker linewidth

powers = two_mean_test.power([-5,-4,-3,-2,-1]) # print power table and get the powers into powers variable

print(powers) # print the powers

one_var_test = hypotest.HypoVarTest(x = sample01, sigma_sqr0 = 36, sig = 0.08, alternative = "right")

print("\n--- Test for one variance done! Results presented bellow. ---\n")
one_var_test.summarize(minimal = True) # See the results

one_var_test.plot_test(colors = {"pdf": "purple", "ts": "orange", "cr": "yellow", "pv": "cyan", "bl": "black"}) # plot the test using a different color scheme
one_var_test.plot_power(np.linspace(36, 100, 1000))

two_var_test = hypotest.HypoVarTest(x = sample01, y = sample02, sigma_sqr0 = 1)

print("\n--- Test for two variances done! Results presented bellow. ---\n")
two_var_test.summarize(minimal = True) # See the results

two_var_test.plot_test(lw = 5) # Plot test

one_prop_test = hypotest.HypoPropTest(p1 = 0.43, n1 = 250, pi0 = 0.4)

print("\n--- Test for one proportion done! Results presented bellow. ---\n")
one_prop_test.summarize() # See the results

one_prop_test.plot_test()

two_prop_test = hypotest.HypoPropTest(p1 = 0.43, p2 = 0.5, n1 = 250, n2 = 300, pi0 = 0, sig = 0.1)

print("\n--- Test for two proportions done! Results presented bellow. ---\n")
two_prop_test.summarize() # See the results

two_prop_test.plot_test(show_values = True) #test statistic and critical value are too close, so we omit these values from the plot
