import numpy as np
import matplotlib.pyplot as plt

# Import data
with open('project_4\\forced_convection\change_fin_height__num_highest_T.txt', 'r') as f:
    lines = f.readlines()
    
temperatures = []
for line in lines:
    temp = line.split(':')[1].strip()
    temperatures.append(float(temp))
temperatures = np.array(temperatures)
temperatures = temperatures.reshape(10, 11)

print(temperatures)


# Plotting
fin_heights = np.linspace(5, 50, 10)
fin_num = np.linspace(20, 30, 11)
fin_num, fin_heights = np.meshgrid(fin_num, fin_heights)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title('Peak Microprocessor Temperature\n vs. Fin Height and Fin Number')
ax.set_xlabel('Fin Height [mm]')
ax.set_ylabel('Fin Number')
ax.set_zlabel('Temperature [$^\circ$C]')
ax.plot_surface(fin_heights, fin_num, temperatures, cmap='viridis')
plt.show()