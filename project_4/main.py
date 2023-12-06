import create_grid as cg
import time


# to prevent multiple axis from showing up, add 1 for each cg.iterate() call
graph_conut = 0 

mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=False, delta=[0.1e-3,0.1e-3], ini_temp=7000)
# mp.get_K(display=False, save=True, name='project_4/only_mp_natural_convection/K.png')
# mp.get_Q(display=False, save=True, name='project_4/only_mp_natural_convection/Q.png')
# mp.iterate(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_natural_convection')

# t0 = time.time()
# mp.iterate(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_natural_convection')
# t1 = time.time()
mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_forced_convection')
# t2 = time.time()
# print(t1-t0, t2-t1)

# checking initial values of the grids
# natural_convection.get_K(display=True)
# with_case.get_Q(display=True)


# with_case = cg.grid(sink_dim=None, nat_conv=True, delta=[0.3e-3,0.3e-3])
# with_case.iterate(max_iterations=10000, save=True, save_every=300, save_folder='no_sink_natural_convection')
# with_sink = cg.grid(nat_conv=True, delta=[0.1e-3,0.1e-3], ini_temp=350)
# with_sink.iterate_K(max_iterations=2000, save=True, save_every=100, save_folder='natural_convection',graph_conut=graph_conut)


# for j in range(10, 40, 5):
#     i = j/100
#     only_mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=False, delta=[i,i])
    # os.mkdir(f'project_4\\only_mp_natural_convection\\delta_{i}')
    # only_mp.iterate(max_iterations=1000, save=True, save_every=100, save_folder=f'only_mp_natural_convection\\delta_{i}')

#

