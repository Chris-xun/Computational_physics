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

# locations are:    TSU, HBK, HER, KMH, data stored in that order
locations = ['TSU', 'HBK', 'HER', 'KMH']

# read data
TSU = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\TSU.csv')
HBK = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\HBK.csv')
HER = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\HER.csv')
KMH = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS2/5_data\KMH.csv')

#x_i = positions of the stations
#x_j = positions of the lines