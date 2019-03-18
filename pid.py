import numpy as np
from matplotlib import pyplot as plt
from control import matlab
import control as ct
import itertools
from scipy import optimize
import math

class System:
    def __init__(self,sys_nums,sys_dens,name,alpha=1):
        self.system = ct.tf(sys_nums,sys_dens)
        self.alpha = alpha
        self.name = name

    #creates PID transfer function
    #arguments are proportional, integration
    #and derivative gains
    def __create_regulator(self,k,Ti,Td):
        return ct.tf([Td,k,Ti],[1,0])

    #returns regulation error for given regulator transfer
    #function system and regulation weight factor
    #alpha should be in range (0,1)
    #default weights are 1 and 0 
    def get_regulation_function(self,kp,kd,ki):
        regulator = self.__create_regulator(kp,ki,kd)
        # creates system with error signal as output
        system_tf = ct.feedback(1,ct.series(self.system,regulator))
        #step response simulation
        e,s = ct.matlab.step(system_tf)
        # return least squares error function with additional parameter
        # reacting for oscilations
        return self.alpha*sum([ x**2 for x in e]) + (1 - self.alpha)*(abs(min(e)/max(e)))
        
    #returns regulation error for given regulator transfer
    #function system and regulation weight factor
    def get_regulation_error(self,params):
        #system coefficients
        k = params[0] # array form required by minimize function from scipy
        Ti = params[1]
        Td = params[2]
        regulator = self.__create_regulator(k,Ti,Td)
        # creates system with error signal as output
        system_tf = ct.feedback(1,ct.series(self.system,regulator))
        # step response simulation
        e,s = ct.matlab.step(system_tf)
        # return least squares error function with additional parameter
        # reacting for oscilations
        return self.alpha*sum([ x**2 for x in e]) + (1-self.alpha)*(abs(min(e)/max(e)))

    def get_function_minimum(self,method):
        #return optimize.minimize(self.get_regulation_error,[1,0,0],bounds=((0,1000),(0,1000),(0,1000)),method=method) #x0 can't be [0,0,0]
        return optimize.minimize(self.get_regulation_error,[1,0,0],method=method) #x0 can't be [0,0,0]