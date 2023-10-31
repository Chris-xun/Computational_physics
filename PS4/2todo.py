# 26.10.2023
import numpy as np
import matplotlib.pyplot as plt
import random as r

def y1(x):
    return np.arccos(1 - 2 * x)

def y2(x, a):
    return a * np.sqrt(x)

def y3(x):
    return np.exp(x)


# part b
def G_y1(x1, x2):
    return np.sqrt(-2 * np.log (x1)) * np.cos(2 * np.pi * x2)

def G_y2(x1, x2):
    return np.sqrt(-2 * np.log (x1)) * np.sin(2 * np.pi * x2)

# i dont get what i actually need to do