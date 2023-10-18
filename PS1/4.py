# 11.10.2023

import numpy as np
import matplotlib.pyplot as plt


def iteration(previous_term, g):
    next_term = 1 - g * previous_term
    return next_term


def approximating(g, print_result=False):
    approx_results = []
    iteration_required = []
    for value in g:
        previous_term = 1
        num_iter = 0
        while num_iter < 10000:
            next_term = iteration(previous_term, value)
            if abs(next_term - previous_term) < 1e-6:
                break
            previous_term = next_term
            num_iter += 1
        if print_result:
            real_value = 1 / (1 + value)
            print("""g = {0:.1f}, approx = {1:.6f}, real = {2:.6f}""".format(
                value, next_term, real_value))
        approx_results.append(next_term)
        iteration_required.append(num_iter)
    if len(approx_results) == 1:
        return approx_results[0]
    return approx_results, iteration_required


def plot(lst):
    # plotting actual values and iterated values
    x = lst
    y_re = 1 / (1 + lst)
    plt.plot(x, y_re, label="real value")
    x = lst
    y_approx, iteration_required = approximating(lst)
    plt.plot(x, y_approx, label="iterated value")
    plt.legend()
    plt.show()

    # plotting error
    x = lst
    y = np.abs(y_re - y_approx)/y_re
    plt.plot(x, y, label="fractional error")
    plt.legend()
    plt.show()

    # plotting number of iterations required
    x = lst
    y = iteration_required
    plt.plot(x, y, label="number of iterations required")
    plt.legend()
    plt.show()


approximating([-0.9, -0.3, 0.5, 0.9, 1.1], print_result=True)
# works for |g|<1, but not for |g|>1


plot(np.linspace(-0.99, 0.99, 100))

# 1/2.1 = 1/1.8 * 1.8/2.1 = 1/1.8 * 1/(2.1/1.8)
# terms                      1     3 [    2    ]
term1 = approximating([0.8])
term2 = term1 * 2.1
term3 = approximating([term2-1])
print('expected', 1/2.1, 'got', term1 * term3)
