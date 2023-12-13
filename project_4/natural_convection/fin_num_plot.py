import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# Import data
temperatures = []
with open('project_4\\natural_convection\\5pt_per_mm\change_fin_num\highest_T.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    temp = line.split(':')[1].strip()
    temperatures.append(float(temp))
temperatures = np.array(temperatures)
temperatures = temperatures + 20

# Plot data
plt.title('Peak Microprocessor Temperature vs. Number of fins')
plt.plot(np.linspace(1,39,39),temperatures, 'x')
plt.grid()
plt.xlabel('Number of fins')
plt.ylabel('Temperature [$^\circ$C]')


# curve fit, looks like a log function
# def f(x, a, b, c):
#     return a*np.exp(-b*x) + c
def f(x, a,b):
    return a*x + b
popt, pcov = opt.curve_fit(f,  np.linspace(20,39,19),  temperatures[20:])
plt.plot(np.linspace(1,39,39), f(np.linspace(1,39,39), *popt))
print(popt)

# plt.show()
#saving plot
plt.savefig('project_4\\natural_convection\\fin_num.png')