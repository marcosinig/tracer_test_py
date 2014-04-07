'''
Created on 7 Apr 2014

@author: marco
'''

import time

class FwCommands():

    def __init__(self, uart):
         self.__uart=uart

    def enable_trace(self):
        self.__uart.write("trace" + " 2")
    
    def disable_trace(self):
        self.__uart.write("trace" + " 0")                        
    
    def enable_atflow(self):
        self.__uart.write("atflow" + " 1")
    
    def disable_atflow(self):
        self.__uart.write("atflow" + " 0")                         
    
    def switchon(self):
        self.__uart.write("sim" + " btns")    
        
    def reset(self):
        self.__uart.write("sim" + " reset")
        
    def help(self):
        self.__uart.write("help")
    
    def gsm(self,str):
        self.__uart.write("uart"+ " " + str)
        
    def startFw(self):
        FwCommands().enable_trace()
        FwCommands().enable_atflow()
        FwCommands().switchon()
        
    def onGsm(self):
        self.__uart.write("gpio 12 0")
        time.sleep(1)
        self.__uart.write("gpio 10 1")
        time.sleep(1)
        self.__uart.write("gpio 10 0")
        time.sleep(1)
 