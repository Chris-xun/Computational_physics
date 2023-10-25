# 24.10.2023
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

r0 = [1,0]
r1 = [np.cos(2*np.pi/3), np.sin(2*np.pi/3)]
r2 = [np.cos(4*np.pi/3), np.sin(4*np.pi/3)]
positions = [r0, r1, r2]

# need to determine x & y via generalised newton raphson method
r =[x,y]

# Define symbolic variables
x, y = sp.symbols('x y')

# Define the function
f = x**2 + y**3

# Calculate partial derivatives symbolically
df_dx = sp.diff(f, x)  # Partial derivative with respect to x
df_dy = sp.diff(f, y)  # Partial derivative with respect to y

E = 0
for position in r:
    electric_term = (r - position) / abs(r - position)**3
    if position == r1:
        electric_term = electric_term / 2
    E += electric_term
    
    
def finding_Jacobian(E, r):
    pass
    
    
    
def newton_raphson(E, r0):
    '''
    E is the electric field
    r0 is the initial guess for position, as a 2d vector
    '''
    # applying newton raphson method to solve E(r) = 0
    ######## x_i_add_1 = x_i - J_matrix_inverse np.dot E_as_a_vector
    return r