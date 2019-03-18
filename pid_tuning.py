import numpy as np
from matplotlib import pyplot as plt 
from control import matlab
import control as ct
import itertools
from scipy.optimize import fmin
import math

#creates feedback system with PID regulator's
#constants and passed object transfer function
def create_pid_tf(kd,kp,ki):
    regulator_num = [kd,kp,ki]
    regulator_den = [1,0]
    return ct.tf(regulator_num,regulator_den)

#returns regulation error for given regulator transfer
#function system and regulation weight factor
#alpha should be in range (0,1)
#default weights are 1 and 0 
def get_regulation_error(regulator,system,alpha=1):
    # creates system with error signal as output
    system_tf = ct.feedback(1,ct.series(system,regulator))
    # step response simulation
    e,s = ct.matlab.step(system)
    # return least squares error function with additional parameter
    # reacting for oscilations
    return alpha*sum(map(lambda x : x**2, e)) + (1-alpha)*(abs(min(e)/max(e)))

#object transfer function numerator and denominator
objects = []
object_num = [ [1],[1],[1],[1],[1],[1],[2,0],[1] ]
object_den = [ [1,1],[1,1.2,0.2],[1,2,5],[1,2,26],[1,0],[2,1,0],[0.5,0.5],[1,1.75,0.875,0.125] ]
sys_names = ['Iner1','Iner2','Osc1','Osc2','Int','DIner','Int','IntIner','Iner3']
#create systems
for i in range(len(object_den)):
    objects.append(ct.tf(object_num[i],object_den[i]))

#regulator's parametrs
kp = np.linspace(0,10,20) #proportional constants
kd = np.linspace(0,10,20) #differentiating constants
ki = np.linspace(0,10,20) #integrating constants

#create empty 3D array
output = np.zeros((len(kp),len(kd),len(ki)))

for i,j,k in zip(range(len(kp)), range(len(kd)), range(len(ki)) ):
    Q = get_regulation_error(create_pid_tf(kd[j],kp[i],ki[k]),objects[0])
    #create 3D list of control error's
    output[i][j][k] = Q
    
print(output)