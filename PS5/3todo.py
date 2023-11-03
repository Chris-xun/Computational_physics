# 01.11.2023
import numpy as np
import matplotlib.pyplot as plt

def analytic(t):
    return t * (t**2 + 2 )/ 6

# part a, let y = dx/dt
def Euler(t = np.linspace(0, 1, 100), x0=0, y0=1/3, plot=False, re = False):
    
    # setting initial values
    dt = t[1] - t[0]
    x = np.zeros(len(t))
    y = np.zeros(len(t))
    x[0] = x0
    y[0] = y0

    # iterating through values
    for i in range(1, len(t)):
        x[i] = x[i-1] + y[i-1] * dt
        y[i] = y[i-1] + t[i-1] * dt
    if plot:
        plotting(t, x, t, analytic(t), 'Euler', 'Analytic')
    if re:
        return x, y
    return x[-1]

def plotting(x1,y1,x2,y2,xlabel, ylabel):
    plt.plot(x1, y1, label = xlabel)
    plt.plot(x2, y2, label = ylabel)
    plt.grid()
    plt.legend()
    plt.show()


# Euler(plot=True)


# part b, shooting method
def shooting(x1, initial_guesses, plotting=False, re=False):
    # applying initial guesses
    G1, G2 = initial_guesses[0], initial_guesses[1]
    R1, R2 = Euler(y0=G1), Euler(y0=G2)
    
    # repeat until stopping condition is met
    iterations = 2
    while True:
        # finding the next guess, using secant method
        gradient = (R2 - R1) / (G2 - G1)
        y_intercept = R2 - G2 * gradient
        G3 = (x1 - y_intercept) / gradient
        R3 = Euler(y0=G3)
                    
        # plotting the result using Euler method using the converged value
        if abs(R3 - x1) < 1e-5:
            print('Converged to initial value of ', G3, ' in ', iterations, ' iterations')
            if plotting:
                x, y = Euler(y0=G3, plot=True)
            break
            
        # updating the variables
        R1, R2, G1, G2 = R2, R3, G2, G3
        
        # for if doent converge
        iterations += 1
        if iterations > 1000:
            raise Exception('Does not converge')
    
    if re:
        x, y = Euler(y0=G3, re=True)
        return x, y
        
# shooting(1/2, [0.1, 1], plotting=True)

##################### checking shooting method #####################
# it shows that error is idential no matter how many sample is used?
# also check what np.var does, i kinda j used it w out checking what it does lol



# part c, using the 'classical physics' second derivative method, assume mass = 1
def classic_solve (t=np.linspace(0,1,100) , N = 100, x0=0, x_N=1/2, re = False):
    dt = t[1] - t[0]
    # generating the inverse of the matrix A, taken from PS
    Ai = np.zeros((N-1,N-1))
    for i in range (0,N-1):
        Ai[i][0]=1+i-N
        Ai [0][i]= Ai[i][0]
        for j in range (1,i+1):
            Ai[i][j]=(j+1)* Ai[i][0]
            Ai[j][i]= Ai[i][j]
    Ai=Ai/N
    
    # generating b vector
    b = np.zeros(N-1)
    b[0] = t[0] * dt**2 - x0
    for i in range(1, len(b)-1):
        b[i] = t[i] * dt**2
    b[-1] = t[-1] * dt**2 - x_N
    
    # multiplying to get x vector
    x = np.matmul(Ai, b)
    # plotting(t[1:], x, t, analytic(t), 'Classical', 'Analytic')
    
    # now getting y0 from x vector
    y0 = (x[1] - x[0]) / dt
    # Euler(t=t, x0=x0, y0=y0, plot=True)
    if re:
        x, y = Euler(t=t, x0=x0, y0=y0, re=True)
        return x, y

classic_solve()




# part d, checking that all the methods are 1st order
def calculate_error(x, y):
    if len(x) != len(y):
        raise Exception('x and y must be of the same length')
    true_values = analytic(x)
    variance = np.var(y - true_values)
    return variance

def checking_order():
    # creating a range of N values, in powers of 2
    num_of_samples = np.logspace(5, 9, 5, base=2, dtype=int)
    print(num_of_samples)
    error_euler = np.array([])
    error_shooting = np.array([])
    error_classic = np.array([])
    
    for N in num_of_samples:
        t = np.linspace(0, 1, N)
        dt = t[1] - t[0]
        x0 = 0
        x_N = 1/2
        
        # Euler
        x, y = Euler(t=t, x0=x0, y0=1/3, re=True)
        error = calculate_error(x, y)
        error_euler = np.append(error_euler, error)
        
        # shooting
        x, y = shooting(x1=x_N, initial_guesses=[0.1, 1], re=True)
        error = calculate_error(x, y)
        error_shooting = np.append(error_shooting, error)
        
        # classical
        x, y = classic_solve(t=t, N=N, x0=x0, x_N=x_N, re=True)
        error = calculate_error(x, y)
        error_classic = np.append(error_classic, error)
        
    # plotting all the errors as functions of N
    plt.plot(num_of_samples, error_euler, label='Euler')
    plt.plot(num_of_samples, error_shooting, label='Shooting')
    plt.plot(num_of_samples, error_classic, label='Classical')
    plt.xlabel('N')
    plt.ylabel('Error')
    plt.legend()
    plt.show()
    
# checking_order()




# part e, again let mass be 1
def classic_solve_2 (t=np.linspace(0,1,100) , N = 100, x0=0, x_N=1/2, re = False):
    dt = t[1] - t[0]
    # generating the inverse of the matrix A, taken from PS
    Ai = np.zeros((N-1,N-1))
    for i in range (0,N-1):
        Ai[i][0]=1+i-N
        Ai [0][i]= Ai[i][0]
        for j in range (1,i+1):
            Ai[i][j]=(j+1)* Ai[i][0]
            Ai[j][i]= Ai[i][j]
    Ai=Ai/N
    
    # generating an initial guess for the iterations, first use a linear guess
    x = t/2
    b = np.zeros(N-1)
    iterations = 0
    
    # iterating until we get the correct solution that goes through both boundry values
    while True:
        # generating/updating b vector
        for i in range(0, len(b)):
            b[i] = (3 * x[i] - t[i] ** 3 / 2) * dt ** 2
        b[0] -= x0
        b[-1] -= x_N
        
        # multiplying to get x vector
        x_new = np.matmul(Ai, b)
        
        # stopping condition, need a better stopping condition
        if abs(x_new[-1] - x[-1]) < 1e-6:
            break
        if iterations > 1000:
            raise Exception('Does not converge')
        
        # updating, parameters and guess of the function
        x = x_new
    
    print(iterations)
    plotting(t[1:], x, t, analytic(t), 'Classical', 'Analytic')
    if re:
        return t[1:], x

# classic_solve_2()




# part f, 4th order Runge-Kutta method   ########################   not working ############################
def RK(t = np.linspace(0, 1, 100), x0=0, y0=1/3, plot=False, re = False):
    
    # setting initial values
    dt = t[1] - t[0]
    x = np.zeros(len(t))
    y = np.zeros(len(t))
    x[0] = x0
    y[0] = y0
    half_step = dt / 2

    # iterating through values
    for i in range(1, len(t)):
        
        fa = y[i-1]
        x_half_later_a = x[i-1] + fa * half_step
        y_half_later_a = x_half_later_a - x[i-1] / half_step
        
        fb = y_half_later_a
        x_half_later_b = x[i-1] + fb * half_step
        y_half_later_b = x_half_later_b - x[i-1] / half_step
        
        fc = y_half_later_b
        x_half_later_c = x[i-1] + fc * half_step
        y_half_later_c = x_half_later_c - x[i-1] / half_step
        
        fd = y_half_later_c
        x_half_later_d = x[i-1] + fd * half_step
        y_half_later_d = x_half_later_d - x[i-1] / half_step
        
        gradient = (fa + 2 * fb + 2 * fc + fd) / 6
        
        x[i] = x[i-1] + gradient * dt
        y[i] = y[i-1] + t[i-1] * dt
    if plot:
        plotting(t, x, t, analytic(t), '4th order RK', 'Analytic')
    if re:
        return x, y
    return x[-1]

RK(plot=True)