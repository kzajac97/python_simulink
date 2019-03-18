from simulink import *
from pid import *
import matlab.engine
import numpy as np
from matplotlib import pyplot as plt 
import control 
import itertools
from threading import Thread
import threading

if __name__ == '__main__':
    systems = [] # empty list of systems
    #list of optimization methods
    methods = ['SLSQP','Nelder-Mead'] #SLSQP is LeastSquares Nelder-Mead is method with no bounds allowed
    weights = [0,0.1,0.2,0.25,0.5,0.75,0.9,1] #list of weights 
    #systems coefficients
    sys_nums = [ [1],[1],[1],[1],[1],[1],[2,0],[1] ]
    sys_dens = [ [1,1],[1,1.2,0.2],[1,2,5],[1,2,26],[1,0],[2,1,0],[0.5,0.5],[1,1.75,0.875,0.125] ]
    sys_names = ['Iner1','Iner2','Osc1','Osc2','Int','DIner','IntIner','Iner3']
    # lists must be equal in size
    if len(sys_nums) is not len(sys_dens):
        print("Wrong number of system coefficients")

    for i in range(len(sys_nums)):
        for weight in weights:
            sys = System(sys_nums[i],sys_dens[i],sys_names[i],weight)
            systems.append(sys)

    def GetMinimum(system,method):
        #Redirect to file when executing 
        #python ./main.py > data.txt 
        minimum = system.get_function_minimum(method)
        print(minimum)
        print(system.name)
        print(system.alpha)
        print(method)

    def GetQFunction(system):
        #coeffs for regulators
        kp = np.linspace(1,10,100) # proportional
        ki = np.linspace(1,10,100) # integrating    
        kd = np.linspace(1,10,100) # differential
        t = np.linspace(0,10,100) # time 
        figures = [0,0,0]
        slices = []
        #empty 3D array
        output = np.zeros((len(kp),len(kd),len(ki)))
        for i,j,k in zip(range(len(kp)),range(len(ki)),range(len(kd)) ):
            Q = system.get_regulation_function(kp[i],ki[j],kd[k])
            output[i][j][k] = Q

        #slice to get x axis only values
        slices.append(np.squeeze(output[:,:1,:1]))
        slices.append(np.squeeze(output[:1,:,:1])) # y axis
        slices.append(np.squeeze(output[:1,:1,:])) # z axis
        
        for i in range(len(figures)):
            figures[i] = plt.figure()
            plt.plot(t,slices[i])
            plt.grid()
            plt.show()
            # save with file names
            fig.savefig(str(system.name)+'.png')


    for system,method in [(system,method) for system in systems for method in methods]:
        thread = Thread(target = GetMinimum, args=(system,method))
        thread.start()
        thread.join()

    for system in systems:
        thread = Thread(target=GetQFunction, args=(system))
        thread.start()
        thread.join()