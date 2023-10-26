# 25.10.2023
import numpy as np
import matplotlib.pyplot as plt

def next_num(x, a, b):
    return (a * x) % b

def generated_variations(generated_numbers, initial_guess):
    if generated_numbers[-1] in generated_numbers[:-1]:
        print('for initial guess', initial_guess, 'period is', len(generated_numbers)-1)
        return True

def iterating(initial_guess, a, b):
    generated_numbers = np.array([initial_guess])
    global max_period
    max_period = 0
    for i in range(100):
        generated_numbers = np.append(generated_numbers, next_num(generated_numbers[-1], a, b))
        if generated_variations(generated_numbers, initial_guess):
            max_period = len(generated_numbers)-1
            break

# part a, by testing we can see that period is at most 11
a, b = 7, 11


# part b, now trying using b = 12, period is only max 3
b = 12

# actually executing the code
for i in range(1, b+2):
    iterating(i, a, b)
    

# then trying using different values of a, we can see that period is at most 4, even for differnt values of initial guess
# a, initial guess, both ranging up to 100
max_periods = np.array([])
for a in range(1, 100):
    max_periods = np.append(max_periods, max_period)
    for initial_guess in range(1, 100):
        iterating(1, a, b)
plt.plot(range(1, 100), max_periods)
plt.show()
