import numpy as np
from matplotlib import pyplot as plt 
from control import matlab
import control as ct
import itertools

def create_system(kd,kp,ki,object_transfer_function):
    regulator_num = [kd,kp,1,ki]
    regulator_den = [1,0]
    regulator_transfer_function = ct.tf(regulator_num,regulator_den)
    #create feedback system with regulation error as output
    return ct.feedback(1,ct.series(object_transfer_function,regulator_transfer_function))


object_num = [1]
object_den = [1,5,3]
obj = ct.tf(object_num,object_den)
kd, kp, ki = 1,1,1
system = create_system(kd,kp,ki,obj)
regulator_num = [kd,kp,1,ki]
regulator_den = [1,0]
regulator_tf = ct.tf(regulator_num,regulator_den)
system2 = ct.feedback(obj,regulator_tf) 
#e is output and t time range
e,t1 = ct.matlab.step(system)
y,t2 = ct.matlab.step(system2)
fig1 = plt.figure() 
plt.plot(t1,e)
plt.grid()
fig1.savefig('plot1.png',bbox_inches='tight')