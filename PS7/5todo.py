# 15.11.2023
import numpy as np
import matplotlib.pyplot as plt


# part a, converting to natural units
def get_rho_g(z,h):
    return np.exp(- z**2/(2 * h**2))

def get_u_z(z,tau,rho_g):
    return -z * tau / rho_g

# part b, upwind method
def upwind(h=0.1, dt=1, tau=1e-4, max_iter=100000, M=2e30, R=1.5e13):
    # initial conditions
    z = np.linspace(0,h,1000)
    dz = z[1] - z[0]
    z = np.append(z, z[-1] + dz)
    rho_g = get_rho_g(z,h)
    rho_d = rho_g/100
    rho_d[-1] = 0    # boundary conditions, no material beyond the boundaries
    velocity = get_u_z(z,tau,rho_g)
    a = np.abs(velocity) * dt / dz
    rho_d_new = np.zeros(len(rho_d)) 
    if max(a) > 1:
        print('Warning: unstable system, a_max = ', max(a))
        
    # evoving the system until a planet is formed
    iterations = 1
    while True:
        
        # each time step
        # for i in range(len(z)-1):
        #     rho_d_new[i] = (1-a[i])*rho_d[i] + a[i+1] * rho_d[i+1]
        # same as above but faster
        rho_d_shifted = np.roll(rho_d_new,-1)
        a_shifted = np.roll(a,-1)
        rho_d_new = (1-a)*rho_d + a_shifted * rho_d_shifted

        # print('iteration',iterations ,': dust',rho_d_new[0], 'gas',rho_g[0])

        # checking for stopping conditions
        if rho_d_new[0] / rho_g[0] > 1:
            print('Planet formed after ', iterations, ' iterations')
            G = 6.6743e-11
            omega = np.sqrt(G * M / (R**3))
            time = iterations * dt / omega
            print('Time to form planet: ', time)
            print('which is ', time / (365 * 24 * 3600e6), ' million years')
            
            break
        if iterations >= max_iter:
            print('Did not converge after ', iterations, ' iterations')
            break
        
        # updating the system
        rho_d = rho_d_new
        iterations += 1
        
# time to form a planet is not affected much by the time step, but does decrease slightly with shorter time steps
upwind()

# part c, according to the simulation, the given planet should take less than 10 million years to form
    # which is much less than the age of the given planetary disk
    # we did not account for diffusion which acts against this process
    
# part d, operator splitting method