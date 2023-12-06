# 02.11.2023
import numpy as np
import matplotlib.pyplot as plt


def analytic(t):
    return np.sin(t)

def Euler(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    E = np.zeros(len(t))
    u[0] = u0
    v[0] = v0
    E[0] = u0 ** 2 + v0 ** 2
    
    for i in range(1, len(t)):
        v[i] = (v[i-1] - u[i-1] * dt) / (dt ** 2 + 1)
        u[i] = (v[i-1] - v[i]) / dt
        E[i] = u[i] ** 2 + v[i] ** 2
    
    if plotting:
        plt.plot(t, u, label = 'Euler')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.plot(t, E, label = 'Energy')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v, E
    
def iterate_Euler(num_of_samples = np.logspace(5, 10, 6, base=2, dtype=int)):
    # repeating Euler method for a range of step sizes
    errors = np.array([])
    for num in num_of_samples:
        t_, u, v_, E_ = Euler(t = np.linspace(0, 1, num), re=True)
        errors = np.append(errors, np.var(u - analytic(t_)))
    plt.loglog(num_of_samples, errors, 'x', label='Euler error (log)')  # straight line, suggest 1st order method
    plt.show()
    plt.plot(num_of_samples, errors, 'x', label='Euler error (linear)')
    plt.show()
    
# Euler(plotting=True)

# now trying using different step sizes
# iterate_Euler()




# part b, implicit Euler
def implicit_Euler(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    E = np.zeros(len(t))
    u[0] = u0
    v[0] = v0
    E[0] = u0 ** 2 + v0 ** 2
    A = np.array([[0 , 1], [-1, 0]])    # update matrix specific to this problem
    G = np.linalg.inv(np.identity(2) - dt * A)    # update matrix specific to this problem, time independent so only need to be calculated once
    
    for i in range(1, len(t)):
        u[i], v[i] = np.dot(G, np.array([u[i-1], v[i-1]]))    # update u and v using the update matrix
        E[i] = u[i] ** 2 + v[i] ** 2
        
    if plotting:
        plt.plot(t, u, label = 'Euler')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.plot(t, E, label = 'Energy')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v, E 

def iterate_Euler_implicity_and_explicit(num_of_samples = np.logspace(5, 10, 6, base=2, dtype=int)):
    # repeating Euler method for a range of step sizes
    errors_implicit = np.array([])
    errors_explicit = np.array([])
    for num in num_of_samples:
        t_, u, v_, E_ = Euler(t = np.linspace(0, 1, num), re=True)
        errors_explicit = np.append(errors_explicit, np.var(u - analytic(t_)))
        t_, u, v_, E_ = implicit_Euler(t = np.linspace(0, 1, num), re=True)
        errors_implicit = np.append(errors_implicit, np.var(u - analytic(t_)))
    plt.loglog(num_of_samples, errors_explicit, 'x', label='Explicit Euler error (log)')  # straight line, suggest 1st order method
    plt.loglog(num_of_samples, errors_implicit, 'o', label='Implicit Euler error (log)')  # straight line, suggest 1st order method
    plt.legend()
    plt.show()
    plt.plot(num_of_samples, errors_explicit, 'x',label='Explicit Euler error (linear)')
    plt.plot(num_of_samples, errors_implicit, 'o', label='Implicit Euler error (linear)')
    plt.legend()
    plt.show()


# implicit_Euler(plotting=True)

# iterate_Euler_implicity_and_explicit()    # the points overlap exactly, as one might expected



# part c, using 'perfect' steps derived from analytic solution to check rounding errors

def perfect_Euler(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
        
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    E = np.zeros(len(t))
    u[0] = u0
    v[0] = v0
    E[0] = u0 ** 2 + v0 ** 2

    for i in range(1, len(t)):
        u[i] = u[i-1] * np.cos(dt) + v[i-1] * np.sin(dt)
        v[i] = v[i-1] * np.cos(dt) - u[i-1] * np.sin(dt)
        E[i] = u[i] ** 2 + v[i] ** 2
        
    if plotting:
        plt.plot(t, u, label = 'Perfect Euler')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.plot(t, E, label = 'Energy')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v, E 

def iterate_perfect_Euler(num_of_samples = np.logspace(3, 11, 9, base=2, dtype=int)):
    # repeating the perfect Euler method for a range of step sizes
    errors = np.array([])
    for num in num_of_samples:
        t_, u, v_, E_ = perfect_Euler(t = np.linspace(0, 1, num), re=True)
        errors = np.append(errors, np.var(u - analytic(t_)))
    plt.plot(num_of_samples, errors, 'x', label='perfect Euler error, only rounding errors')
    plt.legend()
    plt.show()

# perfect_Euler(plotting=True)

# iterate_perfect_Euler()    # the error generally gets worse, but are random



# part d, trying 2nd order methods, and checking if can approach rounding error limit (the process with check that they are 2nd order)
def HOT2(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    u[0] = u0
    v[0] = v0

    for i in range(1, len(t)):
        u[i] = u[i-1] + v[i-1] * dt - 1/2 * u[i-1] * dt ** 2
        v[i] = v[i-1] - u[i-1] * dt - 1/2 * v[i-1] * dt ** 2
        
    if plotting:
        plt.plot(t, u, label = 'HOT2')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v

def AB2(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    u[0] = u0
    v[0] = v0
    u[1] = u[0] * np.cos(dt) + v[0] * np.sin(dt)
    v[1] = v[0] * np.cos(dt) - u[0] * np.sin(dt)

    for i in range(2, len(t)):
        u[i] = u[i-1] + 1/2 * (3 * v[i-1] - v[i-2]) * dt
        v[i] = v[i-1] - 1/2 * (3 * u[i-1] - u[i-2]) * dt
        
    if plotting:
        plt.plot(t, u, label = 'AB2')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v
    
def AM2(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    u[0] = u0
    v[0] = v0
    t_plus = 1 + dt ** 2 / 2
    t_minus = 1 - dt ** 2 / 2
    G = np.array([[t_minus, dt], [-dt, t_minus]]) / t_plus   # update matrix specific to this problem, time independent so only need to be calculated once, calculated by hand

    for i in range(1, len(t)):
        u[i], v[i] = np.dot(G, np.array([u[i-1], v[i-1]]))    # update u and v using the update matrix
        
    if plotting:
        plt.plot(t, u, label = 'AM2')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v
    
    
def f(u_vector):
    u = u_vector[1]
    v = -u_vector[0]
    return np.array([u, v])
    
def RK2(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1, alpha=1/2, plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    u[0] = u0
    v[0] = v0

    for i in range(1, len(t)):
        u_vector = np.array([u[i-1], v[i-1]])
        fa = f(u_vector)
        u_vector_b = u_vector + dt * alpha * fa
        fb = f(u_vector_b)
        u_vector_final = u_vector +  ((2 * alpha - 1 ) * fa + fb) * dt / (2 * alpha)
        u[i], v[i] = u_vector_final[0], u_vector_final[1]
        
    if plotting:
        plt.plot(t, u, label = 'RK2')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v
    
def iterate_second_order(num_of_samples = np.logspace(3, 20, 13, base=2, dtype=int)):
    # repeating the perfect Euler method for a range of step sizes
    errors_HOT2 = np.array([])
    errors_AB2 = np.array([])
    errors_AM2 = np.array([])
    errors_RK2 = np.array([])
    for num in num_of_samples:
        t_, u, v_ = HOT2(t = np.linspace(0, 1, num), re=True)
        errors_HOT2 = np.append(errors_HOT2, np.var(u - analytic(t_)))
        t_, u, v_ = AB2(t = np.linspace(0, 1, num), re=True)
        errors_AB2 = np.append(errors_AB2, np.var(u - analytic(t_)))
        t_, u, v_ = AM2(t = np.linspace(0, 1, num), re=True)
        errors_AM2 = np.append(errors_AM2, np.var(u - analytic(t_)))
        t_, u, v_ = RK2(t = np.linspace(0, 1, num), re=True)
        errors_RK2 = np.append(errors_RK2, np.var(u - analytic(t_)))
    plt.loglog(num_of_samples, errors_HOT2, 'x' , label='HOT2 error')
    plt.loglog(num_of_samples, errors_AB2, 'x', label='AB2 error')
    plt.loglog(num_of_samples, errors_AM2, 'x', label='AM2 error')
    plt.loglog(num_of_samples, errors_RK2, 'x', label='RK2 error')    # HOT2 exactly overlaps with RK2
    plt.xlabel('number of samples')
    plt.ylabel('error magnitude')
    plt.legend()
    plt.show()
    
# iterate_second_order()     # still not reached rounding error limit at > 10**6 samples



# part e, will only impliment RK4
def RK4(t = np.linspace(0, 1, 100), u0 = 0, v0 = 1,  plotting = False, re = False):
    
    # defining arrays and variables
    dt = t[1] - t[0]
    u = np.zeros(len(t))
    v = np.zeros(len(t))
    u[0] = u0
    v[0] = v0

    for i in range(1, len(t)):
        u_vector = np.array([u[i-1], v[i-1]])
        fa = f(u_vector)
        fb = f(u_vector + dt / 2 * fa)
        fc = f(u_vector + dt / 2 * fb)
        fd = f(u_vector + dt * fc)
        u[i], v[i] = u_vector +  (fa + 2*fb + 2*fc + fd) * dt / 6
        
    if plotting:
        plt.plot(t, u,'x' , label = 'RK4')
        plt.plot(t, analytic(t), label = 'Analytic')
        plt.grid()
        plt.legend()
        plt.show()
        
    if re:
        return t, u, v
    
RK4(plotting=True)
    
def iterate_fouth_order(num_of_samples = np.logspace(3, 20, 18, base=2, dtype=int)):
    # repeating the perfect Euler method for a range of step sizes
    errors = np.array([])
    for num in num_of_samples:
        t_, u, v_ = RK4(t = np.linspace(0, 1, num), re=True)
        errors = np.append(errors, np.var(u - analytic(t_)))
    plt.loglog(num_of_samples, errors, 'x', label='RK4 error')
    plt.legend()
    plt.show()

# iterate_fouth_order()
# rounding error dominates around 4000 samples, which corresponds to dt = 0.00025