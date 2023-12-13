import create_grid as cg
import numpy as np
import os
import time


# each block runs independently, only uncomment sections being used

##################################################################################
########################## checks used for debugging #############################
##################################################################################

# t0 = time.time()
# mp.iterate(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_natural_convection')
# t1 = time.time()
# mp.iterate_K(max_iterations=1000, save=True, save_every=1000, save_folder='only_mp_forced_convection')
# t2 = time.time()
# print(t1-t0, t2-t1)

# checking initial values of the grids
# natural_convection.get_K(display=True)
# with_case.get_Q(display=True)



##################################################################################
####################### defining functions & variables ###########################
##################################################################################

# to prevent multiple axis from showing up, add 1 for each cg.iterate() call
graph_count = 0 

# finding initial conditions
def find_ini_T(lower_limit, upper_limit, max_iterations=2000, max_repeat=20, case_dim=None, sink_dim=None, nat_conv=False, delta=[0.1e-3,0.1e-3], v=20, tolerance = 1e-3):
    ''' 
    Tries middle value of the temperature range, then changes upper or lower limit depending on whether the final temperature change is positive or negative,
    the new temperature to try is the middle of the new range. This repeats until the temperature is accurate to 1 kelvin.
    
    This is used to quickly find the initial temperature that will converge under few iterations.
    especially useful for heat sink as each iteration takes a long time.
    
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

        system = cg.grid(case_dim=case_dim, sink_dim=sink_dim, nat_conv=nat_conv, delta=delta, ini_temp=temp_to_try, v=v)
        final_change = system.iterate_K(max_iterations=max_iterations, return_change=True, tolerance=tolerance)
        
        # if converged no need to continue trying
        if final_change == -1:
            return lower_limit, upper_limit, temp_to_try, final_change
    
        # to change upper or lower limit, using only final change
        if final_change > 0:
            lower_limit = temp_to_try
            print('temp tried =', temp_to_try , '\nwas still increasing')
        if final_change < 0:
            upper_limit = temp_to_try
            print('temp tried =', temp_to_try , '\nwas still decreasing')     

        if repeat==max_repeat:
            print('max repeat reached, range is: \n', lower_limit, upper_limit)
            break

        if upper_limit - lower_limit < 1:
            print('accurate to 1 kelvin, range is: \n', lower_limit, upper_limit)
            break

        repeat += 1

    return lower_limit, upper_limit, temp_to_try, final_change


##################################################################################
############################# natural convections #################################
##################################################################################

# for each of the 3 following senarios, 
# first section: using the find_ini_T function to find the optimal initial temperature
# second section: using the predetermined optimal initial temperature to solve

############################### for mp only ###############################
# lower_limit, upper_limit, last_tried = find_ini_T(6000,10000, max_iterations=300, case_dim=None, sink_dim=None, nat_conv=True, max_repeat=10)
# with open('project_4\\only_mp_natural_convection\\ini_T.txt', 'a') as file:
#     string = 'last tried : ' + str(last_tried)
#     file.write(string + '\n')
# mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=True, delta=[0.2e-3,0.2e-3], ini_temp=last_tried)
# mp.iterate_K(max_iterations=100000, save=True, save_every=100000, save_folder='only_mp_natural_convection\\5_pt_per_mm', tolerance=1e-3)


############################### when ceramic case is present ###############################
# lower_limit, upper_limit, last_tried, final_change = find_ini_T(6000,10000, max_iterations=300, case_dim=None, sink_dim=None, nat_conv=True, max_repeat=40, tolerance=1e-5 )
# with open('project_4\\no_sink_natural_convection\\ini_T.txt', 'a') as file:
#     string = 'last tried : ' + str(last_tried)
#     file.write(string + '\n')

# with open('project_4\\no_sink_natural_convection\\ini_T.txt', 'r') as file:
#     last_tried = file.readlines()
# last_tried = float(last_tried[0].split(':')[1].strip())
# with_case = cg.grid(sink_dim=None, nat_conv=True, delta=[0.1e-3,0.1e-3], ini_temp=last_tried)
# with_case.iterate_K(max_iterations=10000, save=True, save_every=10000, save_folder='no_sink_natural_convection', tolerance=1e-3, title='No heat sink, Natural convection')


############################### for heat sink ###############################s
# how number of fins affects the initial temperature
# for i in range (1, 40):
#     lower_limit, upper_limit, last_tried, final_change = find_ini_T(300,8000, max_iterations=300, case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,i], nat_conv=True, max_repeat=40, delta=[1e-3,1e-3], tolerance=1e-5 )
#     with open('project_4\\natural_convection\\ini_T_change_fin_num.txt', 'a') as file:
#         string = 'for fin number = ' + str(i) + ' last tried : ' + str(last_tried) + '  change : ' + str(final_change)
#         file.write(string + '\n')

# with open('project_4\\natural_convection\\ini_T_change_fin_num.txt', 'r') as file:
#     lines = file.readlines()
# last_tried_values = []
# for line in lines:
#     if 'last tried : ' in line:
#         last_tried = line.split(':')[1].strip()
#         last_tried = last_tried.split(' ')[0].strip()
#         last_tried = float(last_tried)
#         last_tried_values.append(last_tried)

# hightest_Ts = []
# for i in range (1, 40):
#     sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,i], nat_conv=True, delta=[0.5e-3,0.5e-3], ini_temp=last_tried_values[i-1])
#     try:
#         os.mkdir(f'project_4\\natural_convection\\5pt_per_mm\\change_fin_num\\fins_{i}')
#     except:
#         pass
#     highest_T = sink.iterate_K(max_iterations=20000, save=True, save_every=20000, save_folder=f'natural_convection\\5pt_per_mm\\change_fin_num\\fins_{i}', return_highest_T=True, tolerance=0.01)
#     hightest_Ts.append(highest_T)
#     graph_count += 1
#     with open('project_4\\natural_convection\\5pt_per_mm\\change_fin_num\\highest_T.txt', 'a') as file:
#         string = 'for fin number = ' + str(i) + ' highest_T : ' + str(highest_T)
#         file.write(string + '\n')

# sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], nat_conv=True, delta=[0.25e-3,0.25e-3], ini_temp=1207.04345703125)
# highest_T = sink.iterate_K(max_iterations=20000, save=True, save_every=20000, save_folder=f'natural_convection\\5pt_per_mm\\change_fin_num\\fins_{20}', return_highest_T=True, tolerance=0.0001, title='Heat sink with 20 fins, Natural convection')

# # how fin height and spacing affects the initial temperature
# fin_heights = [5, 10, 15, 20, 25, 30]
# fin_heights = [i*1e-3 for i in fin_heights]
# fin_spacings = [1, 2, 3, 4]
# fin_spacings = [i*1e-3 for i in fin_spacings]
# for fin_height in fin_heights:
#     for fin_spacing in fin_spacings:
#         lower_limit, upper_limit, last_tried, final_change = find_ini_T(300,8000, max_iterations=300, case_dim=[20e-3,2e-3], sink_dim=[4e-3,fin_height,fin_spacing,1e-3,20], nat_conv=True, max_repeat=40, delta=[1e-3,1e-3], tolerance=1e-5 )
#         with open('project_4\\natural_convection\\ini_T_change_fin_dim.txt', 'a') as file:
#             string = 'for fin height = ' + str(fin_height) + '  for fin spacing = ' + str(fin_spacing)+ ' last tried : ' + str(last_tried) + '  change : ' + str(final_change)
#             file.write(string + '\n')

# with open('project_4\\natural_convection\\ini_T_change_fin_dim.txt', 'r') as file:
#     lines = file.readlines()
# last_tried_values = []
# for line in lines:
#     if 'last tried : ' in line:
#         last_tried = line.split(':')[1].strip()
#         last_tried = last_tried.split(' ')[0].strip()
#         last_tried = float(last_tried)
#         last_tried_values.append(last_tried)
# last_tried_values = np.array(last_tried_values)
# ini_temps = np.reshape(last_tried_values, (6, 4))

# hightest_Ts = np.zeros((6, 4))
# for i in range (0, 6):
#     for j in range (0, 4):
#         sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,(i+1)*5e-3,(j+1)*1e-3,1e-3,20], nat_conv=True, delta=[0.5e-3,0.5e-3], ini_temp=ini_temps[i, j])
#         try:
#             os.mkdir(f'project_4\\natural_convection\\5pt_per_mm\\change_fin_dim\\height_{(i+1)*5}_spacing_{j+1}')
#         except:
#             pass
#         highest_T = sink.iterate_K(max_iterations=100000, save=True, save_every=100000, save_folder=f'natural_convection\\5pt_per_mm\\change_fin_dim\\height_{(i+1)*5}_spacing_{j+1}', return_highest_T=True, tolerance=0.001)
#         hightest_Ts[i, j] = highest_T
#         graph_count += 1
#         with open('project_4\\natural_convection\\5pt_per_mm\\change_fin_dim\\highest_T.txt', 'a') as file:
#             string = 'for fin height = ' + str((i+1)*5) + '  for fin spacing = ' + str(j+1)+ ' highest_T : ' + str(highest_T)
#             file.write(string + '\n')

##################################################################################
############################# forced convections #################################
##################################################################################

# for each of the 3 following senarios, windspeeds of 10, 20, 30, 40, 50, 60, 70, 80, 90, 100m/s were used
# first section: using the find_ini_T function to find the optimal initial temperature
# second section: using the predetermined optimal initial temperatures to solve


############################### for mp only ###############################
# for i in range (1, 11):
#     lower_limit, upper_limit, last_tried = find_ini_T(500,4000, max_iterations=3000, case_dim=None, sink_dim=None, nat_conv=False, max_repeat=10, v=i*10 )
#     with open('project_4\\only_mp_forced_convection\\ini_T.txt', 'a') as file:
#         string = 'for speed v = ' + str(i*10) + ' lower limit is : ' + str(lower_limit) + '  upper limit : ' + str(upper_limit) + ' last tried : ' + str(last_tried)
#         file.write(string + '\n')


# ini_temps = [3800, 2235, 1627, 1311, 1114, 981, 886, 813, 757, 712] 
# for i, ini_temp in zip(range(1, 10), ini_temps):
#     only_mp = cg.grid(case_dim=None, sink_dim=None, nat_conv=False, delta=[0.2e-3,0.2e-3], v=i*10, ini_temp=ini_temp)
#     try:
#         os.mkdir(f'project_4\\only_mp_forced_convection\\5pt_per_mm\\v_{i*10}')
#     except:
#         pass
#     only_mp.iterate_K(max_iterations=1000000, save=True, save_every=10000, save_folder=f'only_mp_forced_convection\\5pt_per_mm\\v_{i*10}',graph_count=graph_count, tolerance=0.1)
#     graph_count += 1


############################### when ceramic case is present ###############################
# for i in range (1, 11):
#     lower_limit, upper_limit, last_tried, final_change = find_ini_T(300, 4000, max_iterations=500, case_dim=[20e-3,2e-3], sink_dim=None, nat_conv=False, max_repeat=10, v=i*10, delta=[0.2e-3,0.2e-3], )
#     with open('project_4\\no_sink_forced_convection\\ini_T.txt', 'a') as file:
#         string = 'for speed v = ' + str(i*10) + ' lower limit is : ' + str(lower_limit) + '  upper limit : ' + str(upper_limit) + '  last tried : ' + str(last_tried) + '  final change : ' + str(final_change)
#         file.write(string + '\n')

# ini_temps = [2612.5, 1542.96875, 1167.1875, 993.75, 820.3125, 733.59375, 675.78125, 646.875, 603.515625, 574.609375]
# for i, ini_temp in zip(range(1, 11), ini_temps):
#     case = cg.grid(case_dim=[20e-3,2e-3], sink_dim=None, nat_conv=False, delta=[0.1e-3,0.1e-3], v=i*10, ini_temp=ini_temp)
#     try:
#         os.mkdir(f'project_4\\no_sink_forced_convection\\10pt_per_mm\\v_{i*10}')
#     except:
#         pass
#     case.iterate_K(max_iterations=1000000, save=True, save_every=10000, save_folder=f'no_sink_forced_convection\\10pt_per_mm\\v_{i*10}',graph_count=graph_count, tolerance=1e-3)
#     graph_count += 1


############################### for heat sink ###############################
# for i in range (1, 11):
#     lower_limit, upper_limit, last_tried, final_change = find_ini_T(300,1000, max_iterations=300, case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], nat_conv=False, max_repeat=40, v=i*10, delta=[1e-3,1e-3], tolerance=1e-5 )
#     with open('project_4\\forced_convection\\ini_T.txt', 'a') as file:
#         string = 'for speed v = ' + str(i*10) + ' lower limit is : ' + str(lower_limit) + '  upper limit : ' + str(upper_limit)+ ' last tried : ' + str(last_tried) + '  final change : ' + str(final_change)
#         file.write(string + '\n')

# ini_temps = [466.11328125, 389.55078125, 360.15625, 345.1171875, 336.23046875, 330.078125, 324.609375, 322.55859375, 319.140625, 316.40625]
# for i, ini_temp in zip(range(1, 11), ini_temps):
#     sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], nat_conv=False, delta=[0.2e-3,0.2e-3], v=i*10, ini_temp=ini_temp)
#     try:
#         os.mkdir(f'project_4\\forced_convection\\5pt_per_mm\\v_{i*10}')
#     except:
#         pass
#     sink.iterate_K(max_iterations=1000000, save=True, save_every=10000, save_folder=f'forced_convection\\5pt_per_mm\\v_{i*10}',graph_count=graph_count, tolerance=1e-2)
#     graph_count += 1


# # it would be interesting to also explore the effect of varying the amount of fins as well as the speed of the wind
# data = np.zeros((40, 10))
# for fin_num in range (1, 41):
#     for wind_speed in range(10, 101, 10):
#         lower_limit, upper_limit, last_tried, final_change = find_ini_T(300,2500, max_iterations=300, case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,fin_num], nat_conv=False, max_repeat=40, v=wind_speed, delta=[1e-3,1e-3], tolerance=1e-5 )
#         data[fin_num-1, int(wind_speed/10-1)] = last_tried
#         with open('project_4\\forced_convection\\ini_T.txt', 'a') as file:
#             string = 'for speed v = ' + str(wind_speed) + '  number of fins = ' + str(fin_num) + ' last tried : ' + str(last_tried) + '  final change : ' + str(final_change)
#             file.write(string + '\n')

# with open('project_4\\forced_convection\\ini_T.txt', 'a') as file:
#     string = str(data)
#     file.write(string + '\n')
    

# getting the last tried values from the ini_T.txt file
with open('project_4\\forced_convection\\ini_T.txt', 'r') as file:
    lines = file.readlines()
last_tried_values = []
for line in lines:
    if 'last tried :' in line:
        last_tried = line.split(':')[1].strip()
        last_tried = float(last_tried.split(' ')[0])
        last_tried_values.append(last_tried)
last_tried_values = np.array(last_tried_values)
ini_temps = np.reshape(last_tried_values, (40, 10))


highest_Ts = np.zeros((40, 10))
for i in range(0, 10):
    for j in range(0, 40):
        if (i == 1 and j == 29):
            ini_temp = ini_temps[j, i]
            sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,j+1], nat_conv=False, delta=[0.5e-3,0.5e-3], v=(i+1)*10, ini_temp=ini_temp)
            try:
                os.mkdir(f'project_4\\forced_convection\\5pt_per_mm\\change_speed__fin\\v_{(i+1)*10}_fins_{j+1}')
            except:
                pass
            highest_T = sink.iterate_K(max_iterations=10000, save=True, save_every=10000, save_folder=f'forced_convection\\5pt_per_mm\\change_speed__fin\\v_{(i+1)*10}_fins_{j+1}' , return_highest_T=True, tolerance=0.001)
            highest_Ts[j, i] = highest_T
            graph_count += 1
            with open('project_4\\forced_convection\\highest_T.txt', 'a') as file:
                string = 'for speed v = ' + str((i+1)*10) + '  number of fins = ' + str(j+1) + ' highest_T : ' + str(highest_T)
                file.write(string + '\n')
print(highest_Ts)
with open('project_4\\forced_convection\\highest_T.txt', 'a') as file:
    string = str(highest_Ts)
    file.write(string + '\n')


## to do
# changing fin heights and number of fins, spacing changed to 1mm, for max heat dissipiation
# for fin_num in range (20, 25):
#     for fin_height in range(5, 51, 5):
#         lower_limit, upper_limit, last_tried, final_change = find_ini_T(300,4000, max_iterations=300, case_dim=[20e-3,2e-3], sink_dim=[4e-3,fin_height*1e-3,1e-3,1e-3,fin_num], nat_conv=False, max_repeat=40, v=20, delta=[1e-3,1e-3], tolerance=1e-5 )
#         with open('project_4\\forced_convection\\ini_T_change_height_num.txt', 'a') as file:
#             string = 'for fin height = ' + str(fin_height) + '  number of fins = ' + str(fin_num) + ' last tried : ' + str(last_tried) + '  final change : ' + str(final_change)
#             file.write(string + '\n')

# with open('project_4\\forced_convection\\ini_T_change_height_num.txt', 'r') as file:
#     lines = file.readlines()
# last_tried_values = []
# for line in lines:
#     if 'last tried :' in line:
#         last_tried = line.split(':')[1].strip()
#         last_tried = float(last_tried.split(' ')[0])
#         last_tried_values.append(last_tried)
# last_tried_values = np.array(last_tried_values)
# ini_temps = np.reshape(last_tried_values, (5,10))
# print(ini_temps)
# highest_Ts = np.zeros((5, 10))
# for i in range(0, 10):
#     for j in range(0, 5):
#         ini_temp = ini_temps[j,i]
#         sink = cg.grid(case_dim=[20e-3,2e-3], sink_dim=[4e-3,(i+1)*5e-3,1e-3,1e-3,j+20], nat_conv=False, delta=[0.5e-3,0.5e-3], v=20, ini_temp=ini_temp)
#         try:
#             os.mkdir(f'project_4\\forced_convection\\5pt_per_mm\\change_fin_height__num\\height_{(i+1)*5}_fins_{j+20}')
#         except:
#             pass
#         highest_T = sink.iterate_K(max_iterations=20000, save=True, save_every=20000, save_folder=f'forced_convection\\5pt_per_mm\\change_fin_height__num\\height_{(i+1)*5}_fins_{j+20}' , return_highest_T=True, tolerance=0.01)
#         highest_Ts[j, i] = highest_T
#         graph_count += 1
#         with open('project_4\\forced_convection\\change_fin_height__num_highest_T.txt', 'a') as file:
#             string = 'for fin height = ' + str((i+1)*5) + '  number of fins = ' + str(j+20) + ' highest_T : ' + str(highest_T)
#             file.write(string + '\n')