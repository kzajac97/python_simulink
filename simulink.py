#!/usr/bin/env python
from __future__ import print_function
import matlab.engine
import os
import itertools

#class holding Simulink Interface for Python
class Simulink:
    #Constructors

    # Default constructor
    def __init__(self):
        self.eng = matlab.engine.start_matlab()

    #Private Methods

    # Runs slx model and returns standard 
    # output vector yout from workspace   
    def __runSlxFileWithOutput(self,sFileName):
        print("Simulation Running")
        self.eng.sim(sFileName)
        return self.eng.workspace['yout']

    # Runs slx model
    def __runSlxFile(self,sFileName):
        print("Simulation Running")
        self.eng.sim(sFileName)
    
    # Public Methods

    # Simulates slx model and saves 
    # its output in workspace
    def Simulate(self,sFileName):
        fileFound = False
        
        files = os.listdir('.')

        for filename in files:
            if filename == sFileName:
                output = self.__runSlxFile(sFileName)
                fileFound = True
    
        if fileFound is False:
            raise FileNotFoundError

    # Simulates slx model with given filename 
    # and returns default yout vector
    def SimulateWithOutput(self,sFileName):
        fileFound = False
        #list of all cwd files
        files = os.listdir('.')

        for filename in files:
            if filename == sFileName:
                output = self.__runSlxFile(sFileName)
                fileFound = True
    
        if fileFound is False:
            raise FileNotFoundError
        #cast result to python array 
        return list(itertools.chain(*output))

    # Returns any matlab variable from current workspace
    def GetFromWorkspace(self,sVarName):
        return self.eng.workspace[sVarName]

    # Casts array returned from matlab 
    # workspace to Python list
    def ArrayToList(self,lst):
        return list(itertools.chain(*lst))

    # Prints current workspace dictionary
    def PrintWorkspace(self):
        print(self.eng.workspace)

    # Finds running MATLAB sessions
    def FindMatlabSessions(self):
        print(matlab.engine.find_matlab())

    # Connects to specified MATLAB session
    def ConnectMatlabSession(self,sSessionName):
        self.eng = matlab.engine.connect_matlab(sSessionName)