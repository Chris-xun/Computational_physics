import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# Import data
temperatures = []
with open('project_4\\forced_convection\highest_T.txt', 'r') as f:
    lines = f.readlines()
lines = lines[41:81]

for line in lines:
    temp = line.split(':')[1].strip()
    temperatures.append(float(temp))
temperatures = np.array(temperatures)
temperatures = temperatures + 20

# Plot data
plt.title('Peak Microprocessor Temperature vs. Number of fins \nfor Forced Convection at 20 $m/s$')
plt.plot(np.linspace(1,40,40),temperatures, 'x')
plt.grid()
plt.xlabel('Number of fins')
plt.ylabel('Temperature [$^\circ$C]')
# plt.show()

# curve fit, looks like a log function
# def f(x, a, b, c):
#     return a*np.exp(-b*x) + c
def f(x, a,b):
    return a*x + b
popt, pcov = opt.curve_fit(f,  np.linspace(15,40,25),  temperatures[15:])
plt.plot(np.linspace(1,40,40), f(np.linspace(1,40,40), *popt))
print(popt)
# plt.show()
#saving plot
plt.savefig('project_4\\forced_convection\\fin_num_20ms.png')