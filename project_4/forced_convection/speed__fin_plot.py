import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import data
tempertures = []
with open('project_4\\forced_convection\highest_T.txt', 'r') as f:
    lines = f.readlines()
lines = lines[1:]
for line in lines:
    temp = line.split(':')[1].strip()
    tempertures.append(float(temp))
temperatures = np.array(tempertures)
temperatures = temperatures + 15
temperatures = temperatures.reshape(10,40)

# print(temperatures)


wind_speed = np.linspace(10, 100, 10) 
fin_num = np.linspace(1, 40, 40)
fin_num, wind_speed = np.meshgrid(fin_num, wind_speed)



# # Plot data
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(fin_num, wind_speed, temperatures, cmap='viridis', edgecolor='none')
ax.set_title('Peak Microprocessor Temperature \nvs. Number of fins and Wind Speed')
ax.set_xlabel('Number of fins')
ax.set_ylabel('Wind Speed $[m/s]$')
ax.set_zlabel('Temperature $[^\circ C]$')
ax.set_zlim(70, 1000)
plt.show()