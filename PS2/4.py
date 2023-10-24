# 24.10.2023
import numpy as np
import matplotlib.pyplot as plt


r0 = [1,0]
r1 = [np.cos(2*np.pi/3), np.sin(2*np.pi/3)]
r2 = [np.cos(4*np.pi/3), np.sin(4*np.pi/3)]
positions = [r0, r1, r2]

# need to determine x & y via generalised newton raphson method
r =[x,y]

E = 0
for position in r:
    electric_term = (r - position) / abs(r - position)**3
    if position == r1:
        electric_term = electric_term / 2
    E += electric_term
    
def newton_raphson(E, r):
    # applying newton raphson method to solve E(r) = 0
    ######## x_i_add_1 = x_i - J_matrix np.dot E_as_a_vector
    return r