# 25.10.2023
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.signal import convolve2d

#np.tanh(T_c / T *(H / H_c + s))
def iterate(s0, H, T, iteration_repeats=1000, return_each = False):
    s_each = np.array([s0])
    iterations = 0
    while True:
        s = np.tanh(1 / T * (H + s0))
        if abs(s - s0) < 1e-6:
            break
        if iterations > iteration_repeats:
            break
        s0 = s
        s_each = np.append(s_each, s)
        iterations += 1
    if return_each:
        return s_each
    return s

def central_diff_scheme(x, y):
    h = abs(x[-1] - x[0]) / (len(x))
    dy = np.zeros(len(x))
    for i in range(1, len(x)-1):
        dy[i] = (y[i+1] - y[i-1]) / (2 * h)
    return x[1:-1], dy[1:-1]

def plot(x,y,xlabel,ylabel):
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

# part a, where we assume H = 0
T = np.linspace(0, 2, 100)
s = np.array([])
for temp in T:
    s = np.append(s, iterate(-0.1, 0, temp)) # convergence is sensitive to sign initial guess, due to shape of tanh graph
E = -s**2
dt, dC = central_diff_scheme(T, E)
#plot(T, s, "T", "M")
#plot(T, E, "T", "E")
#plot(dt, dC, "T", "dE/dT")

# for part c, we range H from -2 to 2 and the otherway around for above and below T_c
T = np.array([-0.5, 0.5])
M = np.linspace(-2, 2, 100)
M_revrsed = np.flip(M)
s_values = np.array([])
for temp in T:
    s = np.array([])
    for mag in M:
        s = np.append(s, iterate(-0.1, mag, temp))
    for mag in M_revrsed:
        s = np.append(s, iterate(0.1, mag, temp))
    s_values = np.append(s_values, s)
#print(s_values)
    #plt.plot(M, s, label="T = {0:.1f}".format(temp))
    #plt.plot(M, E, label="T = {0:.1f}".format(temp))
############### not done ############################
    
    
    
# part d, using monte carlo method
J = 1 * 2 / 4

def create_lattice(w, h): # spin need to be made into +1 & -1
    L = np.random.randint(2, size=(w, h))
    return L * 2 - 1

def calculate_main_spin(lattice):
    lattice = lattice.flatten()
    total_spin = np.sum(lattice)
    return total_spin / len(lattice)

def flipping(L, H):
    # we will go through each electron to decide if we should flip it
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    L = np.pad(L, ((1,1),(1,1)) , mode='constant', constant_values=0)
    for i in range(1, len(L)-1):
        for j in range(1, len(L[0])-1):
            minor = L[i-1:i+2, j-1:j+2]
            result = convolve2d(minor, kernel, mode='valid')
            original_energy = -J/2 * result[0,0] - H * L[i,j]
            flipped_energy = J/2 * result[0,0] - H * L[i,j]
            if flipped_energy < original_energy:
                L[i,j] = -L[i,j]
    return L[1:-1,1:-1]

def energy(sj, si, H):
    return -J * sj * si - H * sj


'''
for t in [1.5, 2.5]:   # this is part e
    s = iterate(calculate_main_spin(L), 0, t, iteration_repeats = 20, return_each=True)
    plot(np.linspace(0, len(s), len(s)), s, "iteration", "average spin at this iteration, at temp " + str(t))
'''
# iterating the flipping process several times and keeping track of the average spin
L= create_lattice(5, 5)
average_spin = np.array([])
for i in range(20):
    L = flipping(L, 0)
    average_spin = np.append(average_spin, calculate_main_spin(L))
plot(np.linspace(0, len(average_spin), len(average_spin)), average_spin, "iteration", "average spin at this iteration")
