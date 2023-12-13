import numpy as np
import matplotlib.pyplot as plt

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
# plt.show()

#saving plot
plt.savefig('project_4\\natural_convection\\fin_num.png')