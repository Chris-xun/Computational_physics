# 25.10.2023
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# defining constants
mu0 = 4*np.pi*1e-7
mu = mu0 / 2 / np.pi
R_E = 6371e3

# function to convert change in longitude or latitude into distance
def convert_to_distance(theta1, theta2):
    thera1 = np.radians(theta1)
    theta2 = np.radians(theta2)
    return abs(theta1 - theta2) * R_E

# function to invert a matrix in steps, could also just use np.linalg.inv() directly
def invert(T):
    det = np.linalg.det(T)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    T_inv = np.transpose(T)
    T_inv = T_inv / det
    return T_inv

def invert_by_gauss_jordan_elimination(M):
    inv = np.identity(len(M))
    for j in range(len(M)): # loop over columns
        # normalising each column and finding the index of the 1 or -1 rows (pivot row)
        column_max = np.amax(np.abs(M[:,j]))
        M[:,j], inv[:,j] = M[:,j]/column_max, inv[:,j]/column_max
        index = np.where((M[:,j] == 1.0) | (M[:,j] == -1.0))[0][0]
        for i in range(len(M)): # loop over rows
            if i != index: # don't act on pivot rows
                M[i,:] -= M[index,:] * M[i,j]
                inv[i,:] -= inv[index,:] * M[i,j]
    return M, inv

# locations are:    HER, HBK, TSU, KMH, data stored in that order
locations = ['HER', 'HBK', 'TSU', 'KMH']

# read data
HER = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\HER.csv')
HBK = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\HBK.csv')
TSU = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\TSU.csv')
KMH = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\KMH.csv')

# calculating T matrix and its inverse, only uses the locations of the existing stations
x = np.array([0, 950, 1700])
y = np.array([150, 1000, 0])

# storing the inverted matrix rather than inverting it every time
h = 1000
xi, xj = np.meshgrid(x, x)
yi, yj = np.meshgrid(y, y)

T_x = mu * h / (h**2 + (xi - xj)**2)
T_x = np.pad(T_x, ((0,3),(0,3)) , mode='constant', constant_values=0)
T_y = mu * h / (h**2 + (yi - yj)**2)
T_y = np.pad(T_y, ((3,0),(3,0)) , mode='constant', constant_values=0)
T = T_x - T_y
print(T * 5e9)
inv = np.linalg.inv(T)
# print(np.array(np.matmul(T, inv), dtype=int))
print(invert_by_gauss_jordan_elimination(T))

