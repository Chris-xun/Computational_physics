# 30.10.2023
import numpy as np
import matplotlib.pyplot as plt
import random as r

# part a
def MC(f, a, b, x):
    '''
    f : object      |   funtion to integrate
    a & b : float   |   limits
    x : array       |   random x values generated
    '''
    V = abs(b - a)
    N = len(x)
    f_x = f(x)
    f_average = sum(f_x) / N
    I = f_average * V
    variance_f = 1 / (N-1) * sum((f_x - f_average)**2)
    variance_I = variance_f * V**2 / N
    return I, np.sqrt(variance_I)


def f(x):
    return np.sin(x**2)/x

# x = np.linspace(0.000000001,10,100)
# I, std = MC(f, 0, 10, x)
# print('integral is: ', I, "\nstandard deviation is:", std)

# to see how standard deviation changes with number of samples, decrease with more samples (duhh)
def iterate_1d():
    for i in range(1, 5):
        N = 10 ** i 
        x = np.linspace(0.000000001,10,N)
        I, std = MC(f, 0, 10, x)
        print('\nfor ', N, 'number of samples, the standard deviation is ', std)




# part c, now to try the same but in more dimensions
def MC_2d(f, a1, b1, a2, b2, x, y):
    '''
    f : object        |   funtion to integrate
    a1 & b1 : float   |   limits in x dimension
    a2 & b2 : float   |   limits in y dimension
    x : array         |   random x values generated
    y : array         |   random y values generated
    '''
    V = abs(b1 - a1) * abs(b2 - a2)
    N = len(x)
    f_x = f_circle(x, y)
    f_average = f_x / N
    I = f_average * V
    variance_f = 1 / (N-1) * (f_x - f_average)**2
    variance_I = variance_f * V**2 / N
    return I, np.sqrt(variance_I)

def f_circle(x_list, y_list, r=1):  # return 1 inside circle, 0 if outside
    num_inside = 0
    for x, y in zip(x_list, y_list):
        if np.sqrt(x**2 + y**2) < r:
            num_inside += 1
    return num_inside

def f_sphere(x, y, r):
    return np.sqrt(r**2 - x**2 - y**2)

I, std = MC_2d(f_circle, 0, 1, 0, 1, np.linspace(-1, 1, 10000), np.linspace(-1, 1, 10000))
print('integral is: ', I, "\nstandard deviation is:", std)