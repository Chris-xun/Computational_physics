import numpy as np
import matplotlib.pyplot as plt
import functions as f

# iterate_K is the improved version of iterate, much faster

class grid():
        
    def __init__(self, mp_dim=[14e-3,1e-3], case_dim=[20e-3,2e-3], sink_dim=[4e-3,30e-3,2e-3,1e-3,20], delta=[0.01e-3,0.01e-3], debug=False, nat_conv=False, ini_temp=400, v=20):
        '''
        mp_dim: dimensions of the microprocessor    [x, y]           | width, thickness
        case_dim: dimensions of the case            [x, y]           | width, thickness
        sink_dim: dimensions of the heat sink       [y, a, b, c, n]  | thinkness, fin length, fin spacing, fin width, num of fins
        delta: grid spacing & time step             [dq, dt]         | space, time, assume equal spatial spacing
        debug: creates test in debug mode           bool             
        nat_conv: forced or natural convection      bool             | forced = False, natural = True
        '''
        
        # setting up class variables
        self.debug = debug
        self.d = delta[0]
        self.nat_conv = nat_conv
        self.T_fig_count = 0
        self.K_fig_count = 0
        self.Q_fig_count = 0
        self.v = v
        
        
        # setting up grid, all in scalled natural units
        # only the microprocessor is present
        if sink_dim is None and case_dim is None:
            nx = int(mp_dim[0] / delta[0])
            ny = int(mp_dim[1] / delta[0])
        # microprocessor and case are present
        elif sink_dim is None and case_dim is not None:
            nx = int(case_dim[0] / delta[0])
            ny = int((case_dim[1] + mp_dim[1]) / delta[0])
        # microprocessor, case and heat sink all present
        else:
            heat_sink_width = int((sink_dim[4]*(sink_dim[2]+sink_dim[3])-sink_dim[2])/delta[0])
            heat_sink_height = int((sink_dim[0]+sink_dim[1])/delta[0])
            ny = int(((case_dim[1]+mp_dim[1]+sink_dim[0]+sink_dim[1])+mp_dim[1])/delta[0])
            if heat_sink_width > case_dim[0]/delta[0]:
                nx = int((sink_dim[4]*(sink_dim[2]+sink_dim[3])-sink_dim[2])/delta[0])
            else:
                nx = int(case_dim[0]/delta[0])
        
        
        # temperature matrix & conductivity matrix & heat source matrix 
        self.T = np.zeros((ny, nx))     # x&y are flipped, due to how arrays are indexed
        self.K = np.zeros((ny, nx))     # x&y are flipped, due to how arrays are indexed
        self.Q = np.zeros((ny, nx))     # x&y are flipped, due to how arrays are indexed
        
        # this is just a guess to start with
        initial_temp = ini_temp - 293.15
        
        # all in scalled natural units
        mp_k = 150
        case_k = 230
        sink_k = 250
        mp_heat_power = 5e8
        d = 1/delta[0]
        
        # only the microprocessor is present
        if sink_dim is None and case_dim is None:
            self.T[:,:] = initial_temp
            self.K[:,:] = mp_k
            self.Q[:,:] = mp_heat_power 
            
        # microprocessor and case are present
        elif sink_dim is None and case_dim is not None:
            self.T[0:int(case_dim[1]*d),0:int(case_dim[0]*d)] = initial_temp
            self.K[0:int(case_dim[1]*d),0:int(case_dim[0]*d)] = case_k
            width_diff = int((case_dim[0]-mp_dim[0])*d)
            left = int(width_diff/2)
            right = left + int(mp_dim[0]*d)
            self.T[int(case_dim[1]*d):, left:right] = initial_temp
            self.K[int(case_dim[1]*d):, left:right] = mp_k
            self.Q[int(case_dim[1]*d):, left:right] = mp_heat_power
            
        # microprocessor, case and heat sink all present
        else:
            # the heat sink is widest element
            if heat_sink_width > case_dim[0]*d:
                # base of heat sink
                self.T[int(sink_dim[1]*d):int((sink_dim[0]+sink_dim[1])*d), :] = initial_temp
                self.K[int(sink_dim[1]*d):int((sink_dim[0]+sink_dim[1])*d), :] = sink_k
                # fins of heat sink
                left = 0
                for i in range(sink_dim[4]):
                    right = left + int(sink_dim[3]*d)
                    self.T[:int(sink_dim[1]*d), left:right] = initial_temp
                    self.K[:int(sink_dim[1]*d), left:right] = sink_k
                    left = right + int(sink_dim[2]*d)
                
                # ceramic case
                width_diff = int(heat_sink_width - case_dim[0]*d)    # for fin & case 
                left = int(width_diff/2)
                right = left + int(case_dim[0]*d)
                self.T[heat_sink_height:int(heat_sink_height+case_dim[1]*d), left:right] = initial_temp
                self.K[heat_sink_height:int(heat_sink_height+case_dim[1]*d), left:right] = case_k
                
                # microprocessor
                width_diff1 = int((case_dim[0]-mp_dim[0]) *d)   # for mp & case
                left1 = int(width_diff1/2) + left
                right1 = left1 + int(mp_dim[0]*d)
                self.T[int(heat_sink_height+case_dim[1]*d):, left1:right1] = initial_temp
                self.K[int(heat_sink_height+case_dim[1]*d):, left1:right1] = mp_k
                self.Q[int(heat_sink_height+case_dim[1]*d):, left1:right1] = mp_heat_power
            
            # the ceramic case is widest element
            else:  
                # ceramic case
                self.T[heat_sink_height:int(heat_sink_height+case_dim[1]*d), :] = initial_temp
                self.K[heat_sink_height:int(heat_sink_height+case_dim[1]*d), :] = case_k
                
                # base of heat sink
                width_diff = int(case_dim[0]*d-heat_sink_width)   # for heat sink & case
                left = int(width_diff/2)
                right = left + heat_sink_width
                self.T[int(sink_dim[1]*d):int((sink_dim[0]+sink_dim[1])*d), left:right] = initial_temp
                self.K[int(sink_dim[1]*d):int((sink_dim[0]+sink_dim[1])*d), left:right] = sink_k
                # fins of heat sink
                for i in range(sink_dim[4]):
                    right = left + int(sink_dim[3]*d)
                    self.T[:int(sink_dim[1]*d), left:right] = initial_temp
                    self.K[:int(sink_dim[1]*d), left:right] = sink_k
                    left = right + int(sink_dim[2]*d)

                # microprocessor
                width_diff = int((case_dim[0]-mp_dim[0]) *d)   # for mp & case
                left = int(width_diff/2)
                right = left + int(mp_dim[0]*d)
                self.T[int(heat_sink_height+case_dim[1]*d):, left:right] = initial_temp
                self.K[int(heat_sink_height+case_dim[1]*d):, left:right] = mp_k
                self.Q[int(heat_sink_height+case_dim[1]*d):, left:right] = mp_heat_power
        
        # padding the matrices with zeros, to allow for boundry conditions
        self.T = np.pad(self.T, (1,1), 'constant', constant_values=0)
        self.K = np.pad(self.K, (1,1), 'constant', constant_values=0)
        self.Q = np.pad(self.Q, (1,1), 'constant', constant_values=0)
            
        
    def get_T(self, display=False, save=False, name='temp.png', graph_count=0, title='Heat map'):
        
        # scaling T back to kelvins
        Temp = np.copy(self.T)
        Temp = Temp + 20   
    
        
        # shows the heat map visually
        if display == True or save == True:
            # masking T, so points in air are not shown
            Temp = Temp[1:-1,1:-1] 
            mask = np.zeros(Temp.shape)
            for i in range(Temp.shape[0]):
                for j in range(Temp.shape[1]):
                    if self.K[i+1, j+1] == 0.0:   # +1 as K is still padded
                        mask[i, j] = 1
            
            plt.figure(str(self.d) + 'T' + str(self.T_fig_count) + str(graph_count))
            plt.title(title)
            # fig, ax = plt.subplots()
            c = plt.imshow(np.ma.masked_array(Temp, mask), cmap='viridis', interpolation='nearest')
            # ax.ticklabel_format(useOffset=False)
            plt.colorbar(c, label='Temp [C]')
            plt.xlabel('x $[mm]$')
            plt.ylabel('y $[mm]$')
            plt.xticks(np.arange(0, Temp.shape[1], 50), np.arange(0, Temp.shape[1], 50)*self.d*1e3)
            plt.yticks(np.arange(0, Temp.shape[0], 20), np.arange(0, Temp.shape[0], 20)*self.d*1e3)
            if self.debug == True:
                for i in range(self.T.shape[0]):
                    for j in range(self.T.shape[1]):
                        plt.text(j, i, Temp[i, j])
            if display == True:
                plt.show()
            if save == True:
                plt.savefig(name)
                plt.close()

        self.T_fig_count += 1
        return self.T
            
                
    def get_K(self, display=False, save=False, name='conductivity.png'):
        # displays and returns the conductivity matrix
        if display == True or save == True:
            plt.figure(str(self.d) + 'K' + str(self.K_fig_count))
            plt.title('Conductivity map')
            plt.imshow(self.K, cmap='bwr', interpolation='nearest', aspect='auto')
            plt.colorbar(label='K')
            if self.debug == True:
                for i in range(self.K.shape[0]):
                    for j in range(self.K.shape[1]):
                        plt.text(j, i, self.K[i, j])
            if display == True:
                plt.show()
            if save == True:
                plt.savefig(name)
                
        self.K_fig_count += 1
        return self.K


    def get_Q(self, display=False, save=False, name='power.png'):
        # displays and returns the heat source matrix
        if display == True or save == True:
            plt.figure(str(self.d) + 'Q' + str(self.Q_fig_count))
            plt.title('Heat source map')
            plt.imshow(self.Q, cmap='bwr', interpolation='nearest', aspect='auto')
            plt.colorbar(label='Q')
            if self.debug == True:
                for i in range(self.Q.shape[0]):
                    for j in range(self.Q.shape[1]):
                        plt.text(j, i, self.Q[i, j])
            if display == True:
                plt.show()
            if save == True:
                plt.savefig(name)
                
        self.Q_fig_count += 1
        return self.Q
    
    
    
    # def operate(self):
    #     # operates the heat sink for 1 interation
        
    #     # new temperature matrix
    #     T_new = np.copy(self.T)
        
    #     # forced convection, this will be overwriten if natural convection
    #     if self.nat_conv == False:
    #         v = 20
    #         h = 11.4 + 5.7*v
    #         # meed tp rewrite fopr forced convection, because it will have different scalling

    #     # iterating over every point in the grid
    #     for i in range(1, self.T.shape[0]-1):
    #         for j in range(1, self.T.shape[1]-1):
                
    #             # getting the minor matrices & variables, that will affect the point
    #             k = np.copy(self.K[i-1:i+2, j-1:j+2])
    #             k_original = np.copy(k)
    #             t = np.copy(self.T[i-1:i+2, j-1:j+2])
    #             q = self.Q[i, j]
    #             # print('before ghosts points are added')
    #             # print('t', t, '\n k', k)
                
    #             # conductivity of 0 is a point in air, which we can safely ignore
    #             if float(k[1, 1]) == 0.0:
    #                 T_new[i, j] = 0.0
    #                 continue
                
    #             # adding the ghost conductivities
    #             if self.nat_conv:
    #                 h = 1.31* (t[1, 1])**(1/3) 

    #             # adding the ghost conductivities 
    #             if k[1, 0] == 0.0:    # boundry to the left
    #                 k[1, 0] = k[1,1]   #h * self.d
    #             if k[1, 2] == 0.0:    # boundry to the right
    #                 k[1, 2] = k[1,1]   #h * self.d
    #             if k[0, 1] == 0.0:    # boundry to the top
    #                 k[0, 1] = k[1,1]   #h * self.d
    #             if k[2, 1] == 0.0:    # boundry to the bottom
    #                 k[2, 1] = k[1,1]   #h * self.d
                 
    #             # calculating the average condutivities   
    #             k1 = f.k(k[1, 1], k[1, 0])  # left
    #             k2 = f.k(k[1, 1], k[1, 2])  # right
    #             k3 = f.k(k[1, 1], k[0, 1])  # top
    #             k4 = f.k(k[1, 1], k[2, 1])  # down
                
    #             # adding the ghost temperatures, now to use k_original as the k minor matrix already has ghost values 
    #             if k_original[1, 0] == 0.0:    # boundry to the left
    #                 phi = f.phi(t[1, 1], h)
    #                 t[1, 0] = t[1, 1] - phi * self.d / k1
    #             if k_original[1, 2] == 0.0:    # boundry to the right
    #                 phi = f.phi(t[1, 1], h)
    #                 t[1, 2] = t[1, 1] - phi * self.d / k2
    #             if k_original[0, 1] == 0.0:    # boundry to the top
    #                 phi = f.phi(t[1, 1], h)
    #                 t[0, 1] = t[1, 1] - phi * self.d / k3
    #             if k_original[2, 1] == 0.0:    # boundry to the bottom
    #                 phi = f.phi(t[1, 1], h)
    #                 t[2, 1] = t[1, 1] - phi * self.d / k4
                
                

                
    #             # calculating the new temperature
    #             new_temp = (self.d**2*q + k1*t[1, 0] + k2*t[1, 2] + k3*t[0, 1] + k4*t[2, 1]) / (k1+k2+k3+k4)
    #             # print('after ghosts points are added')
    #             # print('t', t, '\n k', k)
    #             # print('k1', k1, 'k2', k2, 'k3', k3, 'k4', k4)
    #             # print('new temp is ',new_temp)
    #             # input()
    #             T_new[i, j] = new_temp 

            
    #     # updating the temperature matrix
    #     self.T = np.copy(T_new)
    #     # self.get_T(display=display, save=save, name=name)
    #     # return self.T
      
    #     # operates the heat sink for 1 interation
        
    #     # new temperature matrix
    #     T_new = np.copy(self.T)
        
    #     # forced convection
    #     if self.nat_conv == False:
    #         h = 11.4 + 5.7 * self.v
    #         for i in range(1, self.T.shape[0]-1):
    #             for j in range(1, self.T.shape[1]-1):
                    
    #                 # getting the minor matrices & variables, that will affect the point
    #                 k = np.copy(self.K[i-1:i+2, j-1:j+2])
    #                 t = np.copy(self.T[i-1:i+2, j-1:j+2])
    #                 k_center_value = k[1,1]
    #                 q = self.Q[i, j]
    #                 # print('before ghosts points are added')
    #                 # print('t', t, '\n k', k)
                    
    #                 # conductivity of 0 is a point in air, which we can safely ignore
    #                 if float(k[1, 1]) == 0.0:
    #                     T_new[i, j] = 0.0
    #                     continue
                    
                    
    #                 # within 1 matrial and not on boundry, this 1 first as its the most common case
    #                 if k[1, 0]==k_center_value and k[1,2]==k_center_value and k[0,1]==k_center_value and k[2,1]==k_center_value:
    #                     new_temp = (self.d**2*q+ k_center_value*(t[1, 0] + t[1, 2] + t[0, 1] + t[2, 1])) / (4*k_center_value)
                    
    #                 # if on boundry, then not at interface between materials (there are in fact 4 points that are, but its only 4 out of 10,000 )
    #                 elif k[1, 0]==0.0 or k[1,2]==0 or k[0,1]==0 or k[2,1]==0:
    #                     # adding the ghost points
    #                     phi = f.phi(t[1, 1], h) / k[1, 1]  * self.d
    #                     if k[1, 0] == 0.0:    # boundry to the left
    #                         t[1, 0] = t[1, 1] - phi
    #                     if k[1, 2] == 0.0:    # boundry to the right
    #                         t[1, 2] = t[1, 1] - phi
    #                     if k[0, 1] == 0.0:    # boundry to the top
    #                         t[0, 1] = t[1, 1] - phi
    #                     if k[2, 1] == 0.0:    # boundry to the bottom
    #                         t[2, 1] = t[1, 1] - phi
                            
    #                     # calculating the new temperature
    #                     new_temp = (self.d**2*q+ k_center_value*(t[1, 0] + t[1, 2] + t[0, 1] + t[2, 1])) / (4*k_center_value)
                    
    #                 # if at interface between 2 materials
    #                 else: 
    #                     # calculating the average condutivities, this operation is probs faster than checking which value doesnt match
    #                     k1 = f.k(k[1, 1], k[1, 0])  # left
    #                     k2 = f.k(k[1, 1], k[1, 2])  # right
    #                     k3 = f.k(k[1, 1], k[0, 1])  # top
    #                     k4 = f.k(k[1, 1], k[2, 1])  # down
                        
    #                     # calculating the new temperature
    #                     new_temp = (self.d**2*q+ k1*t[1, 0] + k2*t[1, 2] + k3*t[0, 1] + k4*t[2, 1]) / (k1+k2+k3+k4)
                        
                        
    #                 # print('after ghosts points are added')
    #                 # print('t', t, '\n k', k)
    #                 # print('new temp is ',new_temp)
    #                 # input()
    #                 T_new[i, j] = new_temp 

    #     # natural convection
    #     else:
    #         # iterating over every point in the grid
    #         for i in range(1, self.T.shape[0]-1):
    #             for j in range(1, self.T.shape[1]-1):
                    
    #                 # getting the minor matrices & variables, that will affect the point
    #                 k = np.copy(self.K[i-1:i+2, j-1:j+2])
    #                 t = np.copy(self.T[i-1:i+2, j-1:j+2])
    #                 q = self.Q[i, j]
    #                 # print('before ghosts points are added')
    #                 # print('t', t, '\n k', k)
                    
    #                 # conductivity of 0 is a point in air, which we can safely ignore
    #                 if float(k[1, 1]) == 0.0:
    #                     T_new[i, j] = 0.0
    #                     continue
                        
    #                 # adding the ghost points
    #                 h = 1.31*(t[1, 1])**(1/3) 
    #                 phi = f.phi(t[1, 1], h) / k[1, 1]

    #                 # if on boundry
    #                 if k[1, 0]==0.0 or k[1,2]==0 or k[0,1]==0 or k[2,1]==0:
    #                     if k[1, 0] == 0.0:    # boundry to the left
    #                         k[1, 0] = k[1, 1]
    #                         t[1, 0] = t[1, 1] - phi * self.d
    #                     if k[1, 2] == 0.0:    # boundry to the right
    #                         k[1, 2] = k[1, 1]
    #                         t[1, 2] = t[1, 1] - phi * self.d
    #                     if k[0, 1] == 0.0:    # boundry to the top
    #                         k[0, 1] = k[1, 1]
    #                         t[0, 1] = t[1, 1] - phi * self.d
    #                     if k[2, 1] == 0.0:    # boundry to the bottom
    #                         k[2, 1] = k[1, 1]
    #                         t[2, 1] = t[1, 1] - phi * self.d
                    
    #                 # calculating the average condutivities   
    #                 k1 = f.k(k[1, 1], k[1, 0])  # left
    #                 k2 = f.k(k[1, 1], k[1, 2])  # right
    #                 k3 = f.k(k[1, 1], k[0, 1])  # top
    #                 k4 = f.k(k[1, 1], k[2, 1])  # down
                    
    #                 # print('after ghosts points are added')
    #                 # print('t', t, '\n k', k)
                    
    #                 # calculating the new temperature
    #                 new_temp = (self.d**2*q+ k1*t[1, 0] + k2*t[1, 2] + k3*t[0, 1] + k4*t[2, 1]) / (k1+k2+k3+k4)
    #                 # print('new temp is ',new_temp)
    #                 # input()
    #                 T_new[i, j] = new_temp 

                
    #     # updating the temperature matrix
    #     self.T = np.copy(T_new)
    #     # self.get_T(display=True)
    #     # return self.T
      
    def operate_same_k_in_air(self):
        # operates the heat sink for 1 interation
        
        # new temperature matrix
        T_new = np.copy(self.T)
        
        # forced convection
        if self.nat_conv == False:
            h = 11.4 + 5.7 * self.v
            for i in range(1, self.T.shape[0]-1):
                for j in range(1, self.T.shape[1]-1):
                    
                    # getting the minor matrices & variables, that will affect the point
                    k = np.copy(self.K[i-1:i+2, j-1:j+2])
                    t = np.copy(self.T[i-1:i+2, j-1:j+2])
                    q = self.Q[i, j]
                    # print('before ghosts points are added')
                    # print('t', t, '\n k', k)
                    
                    # conductivity of 0 is a point in air, which we can safely ignore
                    if float(k[1, 1]) == 0.0:
                        T_new[i, j] = 0.0
                        continue
                    
                    # adding the ghost points
                    phi = f.phi(t[1, 1], h) / k[1, 1]

                    # if on boundry
                    if k[1, 0]==0.0 or k[1,2]==0 or k[0,1]==0 or k[2,1]==0:
                        if k[1, 0] == 0.0:    # boundry to the left
                            k[1, 0] = k[1, 1]
                            t[1, 0] = t[1, 1] - phi * self.d
                        if k[1, 2] == 0.0:    # boundry to the right
                            k[1, 2] = k[1, 1]
                            t[1, 2] = t[1, 1] - phi * self.d
                        if k[0, 1] == 0.0:    # boundry to the top
                            k[0, 1] = k[1, 1]
                            t[0, 1] = t[1, 1] - phi * self.d
                        if k[2, 1] == 0.0:    # boundry to the bottom
                            k[2, 1] = k[1, 1]
                            t[2, 1] = t[1, 1] - phi * self.d
                    
                    # calculating the average condutivities   
                    k1 = f.k(k[1, 1], k[1, 0])  # left
                    k2 = f.k(k[1, 1], k[1, 2])  # right
                    k3 = f.k(k[1, 1], k[0, 1])  # top
                    k4 = f.k(k[1, 1], k[2, 1])  # down
                    
                    # print('after ghosts points are added')
                    # print('t', t, '\n k', k)
                    
                    # calculating the new temperature
                    new_temp = (self.d**2*q+ k1*t[1, 0] + k2*t[1, 2] + k3*t[0, 1] + k4*t[2, 1]) / (k1+k2+k3+k4)

                    # print('new temp is ',new_temp)
                    # input()
                    T_new[i, j] = new_temp 

        # natural convection
        else:
            # iterating over every point in the grid
            for i in range(1, self.T.shape[0]-1):
                for j in range(1, self.T.shape[1]-1):
                    
                    # getting the minor matrices & variables, that will affect the point
                    k = np.copy(self.K[i-1:i+2, j-1:j+2])
                    t = np.copy(self.T[i-1:i+2, j-1:j+2])
                    q = self.Q[i, j]
                    # print('before ghosts points are added')
                    # print('t', t, '\n k', k)
                    
                    # conductivity of 0 is a point in air, which we can safely ignore
                    if float(k[1, 1]) == 0.0:
                        T_new[i, j] = 0.0
                        continue
                        
                    # adding the ghost points
                    h = 1.31*(t[1, 1])**(1/3) 
                    phi = f.phi(t[1, 1], h) / k[1, 1]

                    # if on boundry
                    if k[1, 0]==0.0 or k[1,2]==0 or k[0,1]==0 or k[2,1]==0:
                        if k[1, 0] == 0.0:    # boundry to the left
                            k[1, 0] = k[1, 1]
                            t[1, 0] = t[1, 1] - phi * self.d
                        if k[1, 2] == 0.0:    # boundry to the right
                            k[1, 2] = k[1, 1]
                            t[1, 2] = t[1, 1] - phi * self.d
                        if k[0, 1] == 0.0:    # boundry to the top
                            k[0, 1] = k[1, 1]
                            t[0, 1] = t[1, 1] - phi * self.d
                        if k[2, 1] == 0.0:    # boundry to the bottom
                            k[2, 1] = k[1, 1]
                            t[2, 1] = t[1, 1] - phi * self.d
                    
                    # calculating the average condutivities   
                    k1 = f.k(k[1, 1], k[1, 0])  # left
                    k2 = f.k(k[1, 1], k[1, 2])  # right
                    k3 = f.k(k[1, 1], k[0, 1])  # top
                    k4 = f.k(k[1, 1], k[2, 1])  # down
                    
                    # print('after ghosts points are added')
                    # print('t', t, '\n k', k)
                    
                    # calculating the new temperature
                    new_temp = (self.d**2*q+ k1*t[1, 0] + k2*t[1, 2] + k3*t[0, 1] + k4*t[2, 1]) / (k1+k2+k3+k4)
                    # print('new temp is ',new_temp)
                    # input()
                    T_new[i, j] = new_temp 

                
        # updating the temperature matrix
        self.T = np.copy(T_new)
        # self.get_T(display=True)
        # return self.T
        
        
    # def iterate(self, max_iterations=1000, tolerance=1e-3, save=False, save_every=100, save_folder=None, graph_count=0, return_=False):
    #     # iterates the heat sink for a given number of iterations
    #     iteration = 0
    #     if save==True:
    #         self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png')
        
    #     total_energy = np.sum(self.T)
        
    #     while True:
            
    #         # operating
    #         self.operate()
    #         iteration += 1
    #         print('iteration', iteration)
            
    #         # checking if max iterations reached
    #         if iteration == max_iterations:
    #             print('Did not converge after', iteration, 'iterations')
    #             if save == True:
    #                 self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count)
    #             break
            
    #         # checking for convergence
    #         new_total_energy = np.sum(self.T)
    #         change = np.abs(new_total_energy - total_energy)
    #         if change < tolerance:
    #             print('Converged after', iteration, 'iterations')
    #             if save == True:
    #                 self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count)
    #             break
    #         total_energy = new_total_energy
            
    #         # saving at every given interval
    #         if save==True and iteration % save_every == 0:
    #             print('iteration', iteration)
    #             self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count)

    #         if abs(iteration - max_iterations/2) <= 1:
    #             total_energy_middle = np.sum(self.T)

    #     if return_:
    #         total_energy_final = np.sum(self.T)
    #         return total_energy_middle, total_energy_final
        
    def iterate_K(self, max_iterations=1000, tolerance=1e-3, save=False, save_every=100, save_folder=None, graph_count=0, return_change=False, return_highest_T=False, title='Heat map'):
        # iterates the heat sink for a given number of iterations
        iteration = 0
        if save==True:
            self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png')
        
        total_energy = np.sum(self.T)
        previous_change = 10000

        while True:
            
            # operating
            self.operate_same_k_in_air()
            iteration += 1
            
            # checking if max iterations reached
            if iteration == max_iterations:
                print('Did not converge after', iteration, 'iterations')
                if save == True:
                    self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count, title=title)
                break
            
            # checking for convergence
            new_total_energy = np.sum(self.T)
            change = new_total_energy - total_energy
            if (abs(change) < tolerance and iteration > 12345) or (iteration>5000 and abs(change) > abs(previous_change)):
                # setting  minimum number of iterations to make sure it has converged
                # also checking if the change is increasing, if so, then it has already reached the minimum
                print('Converged after', iteration, 'iterations')
                if save == True:
                    self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count, title=title)
                if return_change:
                    return -1
                break
            total_energy = new_total_energy
            previous_change = change
            
            # saving at every given interval
            if save==True and iteration % save_every == 0:
                # print('iteration', iteration, 'change', change)
                self.get_T(save=True, name='project_4/'+str(save_folder)+'/after_'+str(iteration)+'_iterations.png', graph_count=graph_count, title=title)
            
            print('iteration', iteration, 'change', change)

        if return_change:
            return change
        
        if return_highest_T:
            return np.max(self.T)
