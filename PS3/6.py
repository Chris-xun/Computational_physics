# 18.10.2023
import numpy as np
import matplotlib.pyplot as plt


def DFT(f, t):
    N = len(f)
    T = t[-1] - t[0]
    F = np.zeros(N, dtype=complex)
    w = np.zeros(N)
    # for p in range(int(-1 * N / 2), int(N / 2 + 1), 1):
    for p in range(N):
        for n in range(N):
            F[p] += f[n] * np.exp(-2j * np.pi * p * n / N)
        if p != 0:
            F[p] = F[p] / (t[p] - t[p-1])
        w[p] = p * 2 * np.pi / T

    # print(w)
    #w = np.array([*w[int(N/2+1):], *w[:int(N/2+1)]])
    print('the smallest change in angular frequency that can be resolved is', 2 * np.pi / T)
    return F, w


def plotting(x, y, x_label='x', y_label='y'):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def find_diff_between_peaks(x, y):
    peaks_x = []
    diff = []
    for i in range(len(y)):
        if y[i] > 1:
            peaks_x.append(x[i])
    for i in range(len(peaks_x)-1):
        diff.append(peaks_x[i+1] - peaks_x[i])

    return diff


def create_gaussian(x, sigma, mu):
    # gaussian has to be created to be periodic from 0 to T
    half = int(len(x) / 2)
    y = 1 / (sigma * np.sqrt(2 * np.pi)) * \
        np.exp(-1 * (x - mu)**2 / (2 * sigma**2))
    return np.array([*y[half:], *y[:half]])


'''
# testing with sin wave
x = np.linspace(0, 10*np.pi, 2**10)
y = np.sin(x)
plotting(x, y, y_label='sin x')
DFT(y, x)
'''


# DFT for data
time, function = np.loadtxt('data_6.txt', unpack=True)
plotting(time, function, 'time', 'function')

DFT_of_function, angular_frequency = DFT(function, time)
DFT_of_function, angular_frequency = DFT_of_function[:50], angular_frequency[:50]
w_unit = 1 / 1e-12
# value at 0 frequency because the function has non zero average
plotting(angular_frequency, DFT_of_function,
         'angular frequency, $10^{12}$ rad/s', 'DFT of function')

diff = find_diff_between_peaks(angular_frequency, DFT_of_function)
diff = 0.75205693e12    # diff found to be 0.75205693e12
h_bar = 1.054571817e-34
Energy = h_bar * diff
B_0 = Energy / (1 * (1 + 1))    # = 3.965490215787709e-23, for 1st peak
# The diatomic molecule is Nitrogen


# creating gussians for
x = np.linspace(-1, 1, 1000)
y = create_gaussian(x, 0.1, 0)    # using units of picoseconds (1e-12)
plotting(x, y, 'time, $10^{-12}$ s', 'normalised gaussian')
DFT_of_gaussian, angular_frequency_gaussian = DFT(y, x)
G_half = int(len(DFT_of_gaussian)/2)
DFT_of_gaussian = np.array(
    [*DFT_of_gaussian[G_half:], *DFT_of_gaussian[:G_half]])
# reconstructed to display the gaussian the usual way
plt.xlim(1500, 1650)
plotting(angular_frequency_gaussian, DFT_of_gaussian,
         'angular frequency, $10^{12}$ rad/s', 'DFT of gaussian')
