# 08.11.2023
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing data
df = pd.read_csv('C:/Users\yx200\Desktop\imperial\yr3\computational_physics\PS6\events.csv')
# df_2to3 = df[(df['q2'] > 2) & (df['q2'] < 3)]
# print(df_2to3)

df_list = [df[(df['q2'] > i+1) & (df['q2'] < i+2)] for i in range(0,7)]
# print(df_list)

def plot_hist(r=[0,-1], plotting = False):
    
    # taking out the datas to plot
    data_to_plot = df_list[r[0]:r[1]]
    if r == [0,-1]:
        data_to_plot = df_list
        
    for i, df_section in zip(range(1,8), data_to_plot):
        n, bins = np.histogram(df_section['costhetak'], bins=10, density = True)
        uncert = np.sqrt(n * 5 / df_section.shape[0])
        bin_centers = 0.5*(bins[1:] + bins[:-1])
        if plotting:
            plt.hist(df_section['costhetak'], bins=10, density = True)       
            plt.errorbar(bin_centers, n, yerr=uncert, fmt='.', capsize=3)
            plt.title('in region ' + str(i) + ' < q^2 < ' + str(i+1) + ' GeV^2/c^4')
            plt.ylabel('number of events')
            plt.xlabel('cos(theta_k)')
            plt.show()
        return n, bin_centers, uncert
        
def function(N, alpha, costhetaK):
    sin2thetaK = 2 * costhetaK * np.sqrt(1 - costhetaK**2)
    return N * (1 + alpha * sin2thetaK)

def integrate_1d(f, x, a, b, alpha):
    V = abs(b - a)
    f_x = f(1, alpha, x)
    f_average = sum(f_x) / len(x)
    I = f_average * V
    Normalisation = 1 / I
    return Normalisation, I
    
def chi_squared(alpha, costhetaK, y, sigma):
    f = function(1/2, alpha, costhetaK)    # as we worked out N = 1/2
    return sum( ((y-f)/sigma)**2 )

def gradient_decend(r=[1,-1], d=1e-4, tolerence = 1e-5, max_iteration = 1000):
    # initial values
    alpha = 1e-4
    iterations = 0
    y, x, sigma = plot_hist(r=r, plotting=False)   # y: normalised frquency, x: the bin centers, sigma: the uncertainty of y
    
    while True:
        # finding gradient of chi squared, as a function of alpha
        gradient = (chi_squared(alpha+d, x, y, sigma) - chi_squared(alpha, x, y, sigma) ) / d    
        new_alpha = alpha - d * gradient
        
        iterations += 1
        if abs(new_alpha - alpha) < tolerence:
            print('converged to ', new_alpha, ' after ', iterations, ' iterations')
            return new_alpha
        if iterations >= max_iteration:
            print('did not converge after ', iterations, ' iterations')
            break
        
        alpha = new_alpha
    

def S5 (alpha):
    return 2 * alpha / 3

def plot_S5(plotting = False):
    S5_list = []
    q2_list = [i + 0.5 for i in range(1,8)]
    for i in range(0,7):
        alpha = gradient_decend(r=[i,i+1])
        S5_list.append(S5(alpha))
    if plotting:
        plt.title('S5 as a function of q^2')
        plt.xlabel('q^2')
        plt.ylabel('S5')
        plt.plot(q2_list, S5_list)
        plt.show()

def cubic_spline():
    # cubic spline
    pass


# part a
# plot_hist(1, plotting=True)

# part b, normalisatin factor N found to be 0.5
# N, I_ = integrate_1d(function, np.linspace(-1,1,1000), -1, 1, 2) 

# part c, gradient decent method
# gradient_decend()

# part d, using differnt step size
# step sizes too big or too small will diverge; overshoot or too slow respectively

# part e, plotting S5 as a function of q^2
# plot_S5(plotting=True)

# part f, using cubic spline to estimate S5 at q^2 = 0
