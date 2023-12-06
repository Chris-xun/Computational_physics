import create_grid as cg
import os
import time


# to prevent multiple axis from showing up, add 1 for each cg.iterate() call
graph_count = 0 

mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3], ini_temp=8969)    # 80000> natural > 8000
# mp.get_K(display=False, save=True, name='project_4/only_mp_natural_convection/K.png')
# mp.get_Q(display=False, save=True, name='project_4/only_mp_natural_convection/Q.png')
mp.iterate_K(max_iterations=100000, save=True, save_every=1000, save_folder='only_mp_natural_convection', tolerance=1e-3)

# t0 = time.time()
# mp.iterate(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_natural_convection')
# t1 = time.time()
# mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_forced_convection')
# t2 = time.time()
# print(t1-t0, t2-t1)

# checking initial values of the grids
# natural_convection.get_K(display=True)
# with_case.get_Q(display=True)


# with_case = cg.grid(sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3], ini_temp=7462)
# with_case.iterate_K(max_iterations=10000, save=True, save_every=300, save_folder='no_sink_natural_convection')
# with_sink = cg.grid(nat_conv=False, delta=[0.1e-3,0.1e-3], ini_temp=350)
# with_sink.iterate_K(max_iterations=2000, save=True, save_every=100, save_folder='forced_convection',graph_count=graph_count)


# for i in range(1, 10):
#     only_mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=False, delta=[0.1e-3,0.1e-3], v=i*10)
#     try:
#         os.mkdir(f'project_4\\only_mp_forced_convection\\v_{i*10}')
#     except:
#         pass
#     only_mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder=f'only_mp_forced_convection\\v_{i*10}',graph_count=graph_count)
#     graph_count += 1



finding initial conditions
def find_ini_T(lower_limit, upper_limit, max_iterations=2000, max_repeat=1000, case_dim=None, sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3]):
    '''
    lower_limit
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

find_ini_T(7400,7500, case_dim=[20e-3,2e-3])