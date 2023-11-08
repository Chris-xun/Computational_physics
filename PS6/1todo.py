# 07.11.2023
import numpy as np
import matplotlib.pyplot as plt


def f(x, a):
    return -np.exp(-1*(x[0]**2 + a*x[1]**2))

# am i supposed to work the derivatives out by hand? or suppose to use a finite difference scheme?

def Newton(x0, a, d=1e-5):
    """_summary_

    Args:
        d_guess (numpy array): guess of [change in x, change in y]
        x0 (numpy array): [initial x, initial y]
        a (float): a constant used in f
    """
    iterations = 0
    while True:
        del_f = np.zeros(2)
        H = np.zeros((2,2))
        
        # change in either direction
        d1 = np.array([x0[0] + d, x0[1]])
        d2 = np.array([x0[0], x0[1] + d])    
        change = np.array([d1, d2])    # the new values of x & y
        
        # finding gradient
        for i in range(2):
            del_f[i] = (f(change[i],a) - f(x0,a)) / d
        
        # finding the Hessian matrix
        H[0][0] = (f(d1,a) - f(x0,a) - del_f[0]*d) *2/d**2
        H[1][1] = (f(d2,a) - f(x0,a) - del_f[1]*d) *2/d**2
        off_diag_value = (f(d2,a) - f(x0,a) - del_f[0]*d) *2/d**2    # order of partial derivatives doesn't matter
        H[0][1], H[1][0] = off_diag_value, off_diag_value
        
        print(off_diag_value, (f(d1,a) - f(x0,a) - del_f[1]*d) *2/d**2)  
        
        iterations += 1
        if iterations > 1:
            print('Did not converge after ', iterations, ' iterations')
            break
        
Newton(np.array([1, 1]), 6)

print('------------------')
print(f(np.array([1,1]), 1))