import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Import data
tempertures = []
with open('project_4\\natural_convection\\5pt_per_mm\change_fin_dim\highest_T.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    temp = line.split(':')[1].strip()
    tempertures.append(float(temp))
temperatures = np.array(tempertures)
temperatures = temperatures + 20
temperatures = temperatures.reshape(4,6)

print(temperatures)

t = np.linspace(1000, 3000, 6)
fin_heights = np.linspace(5, 30, 6) 
print(fin_heights)
fin_separation = np.linspace(4, 1, 4)
fin_heights, fin_separation = np.meshgrid(fin_heights, fin_separation)
# fin_heights = fin_heights.flatten()
# fin_separation = fin_separation.flatten()


# Plot data
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title('Peak Microprocessor Temperature\n vs. Fin Dimensions')
ax.set_xlabel('Fin Height [mm]')
ax.set_ylabel('Fin Separation [mm]')
# ax.set_yticks(fin_separation.flatten())
# ax.set_xticks(fin_heights.flatten())
ax.set_zlabel('Temperature [$^\circ$C]')
# ax.set_zticks(t)
ax.plot_surface(fin_heights, fin_separation, temperatures, cmap='viridis')
plt.show()

# #saving plot
# plt.savefig('project_4\\natural_convection\\fin_dim_plot.png', dpi=300)