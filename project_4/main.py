import create_grid as cg
import numpy as np
import os
import time
# from numba import jit


# to prevent multiple axis from showing up, add 1 for each cg.iterate() call
graph_count = 0 

# mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3], ini_temp=8000)   # 8969
# # mp.get_K(display=False, save=True, name='project_4/only_mp_natural_convection/K.png')
# # mp.get_Q(display=False, save=True, name='project_4/only_mp_natural_convection/Q.png')
# mp.iterate_K(max_iterations=100000, save=True, save_every=1000, save_folder='only_mp_natural_convection', tolerance=1e-3)

# t0 = time.time()
# mp.iterate(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_natural_convection')
# t1 = time.time()
# mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_forced_convection')
# t2 = time.time()
# print(t1-t0, t2-t1)

# checking initial values of the grids
# natural_convection.get_K(display=True)
# with_case.get_Q(display=True)


# with_case = cg.grid(sink_dim=None, nat_conv=False, delta=[0.05e-3,0.05e-3], ini_temp=1750)
# with_case.iterate_K(max_iterations=10000, save=True, save_every=100, save_folder='no_sink_forced_convection')
with_sink = cg.grid(nat_conv=True, delta=[0.1e-3,0.1e-3],  ini_temp=355)
with_sink.iterate_K(max_iterations=2000000, save=True, save_every=1000, save_folder='natural_convection\\2pt_per_mm',graph_count=graph_count)


# for i in range(1, 10):
#     only_mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=False, delta=[0.1e-3,0.1e-3], v=i*10)
#     try:
#         os.mkdir(f'project_4\\only_mp_forced_convection\\v_{i*10}')
#     except:
#         pass
#     only_mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder=f'only_mp_forced_convection\\v_{i*10}',graph_count=graph_count)
#     graph_count += 1



# finding initial conditions
def find_ini_T(lower_limit, upper_limit, max_iterations=2000, max_repeat=20, case_dim=None, sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3], v=20):
    ''' 
    Tries middle value of the temperature range, then changes upper or lower limit depending on whether the temperature is increasing or decreasing,
    the new temperature to try is the middle of the new range. This repeats until the temperature is accurate to 1 kelvin.
    
    lower_limit: lower limit of the temperature range to trial from
    upper_limit: upper limit of the temperature range to trial from
    max_iterations: maximum number of iterations to run at each teamperature
    max_repeat: maximum number of temperatures to try
    case_dim: dimensions of the case
    sink_dim: dimensions of the sink
    nat_conv: whether the system has natural convection
    delta: grid spacing
    '''

    repeat = 0
    while True:
        temp_to_try = (lower_limit + upper_limit)/2

        # if upper and lower limits were wrong
        if temp_to_try - lower_limit < 1:
            print('lower limit was too high')
            break
        if upper_limit - temp_to_try < 1:
            print('upper limit was too low')
            break

        system = cg.grid(case_dim=case_dim, sink_dim=sink_dim, nat_conv=nat_conv, delta=delta, ini_temp=temp_to_try)
        mid, fin = system.iterate_K(max_iterations=max_iterations, return_=True)
        change = fin - mid
        print(change)

        # to change upper or lower limit
        if change > 0:
            lower_limit = temp_to_try
            print('temp tried =', temp_to_try , '\nwas still increasing')
        if change < 0:
            upper_limit = temp_to_try
            print('temp tried =', temp_to_try , '\nwas still decreasing')

        if repeat==max_repeat:
            print('max repeat reached, range is: \n', lower_limit, upper_limit)
            break

        if upper_limit - lower_limit < 1:
            print('accurate to 1 kelvin, range is: \n', lower_limit, upper_limit)
            break

        repeat += 1

    return lower_limit, upper_limit

# find_ini_T(650,700, case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], max_iterations=500, max_repeat=5 )   #  T>almost700?
# find_ini_T(500,3000, case_dim=[20e-3,2e-3], max_iterations=500, nat_conv=False, max_repeat=5 )

# run one for forced convection overnight  v=10*i  i 1to10, use 500 iteration insted of 2000
# please please plesae test the storing results in an array before using 
# try if convergence temp is different if more or less data points is used


# # check to remove axis offsets
# lower_limits = []
# upper_limits = []
# for i in range (6, 11):
#     lower_limit, upper_limit = find_ini_T(100,1000, max_iterations=500, case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], nat_conv=False, max_repeat=10, v=i*10 )
#     lower_limits.append(lower_limit)
#     upper_limits.append(upper_limit)
#     with open('project_4\\ini_T.txt', 'a') as file:
#         string = 'for speed v = ' + str(i*10) + ' lower limit is : ' + str(lower_limit) + '  upper limit : ' + str(upper_limit)
#         file.write(string + '\n')
    
# print('lower limits are :', lower_limits)
# print('upper limits are :', upper_limits)