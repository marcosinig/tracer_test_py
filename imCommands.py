'''
Created on 7 Apr 2014

@author: marco
'''

import time
import re
import sys

from imUtils import *

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
        

class EventMsg():
    def __init__(self, line, event, str1=""):
        self.line=line
        self.event=event
        self.str1 = str1
        

class ShellEvents(Observable, Parseble):
    """
    todo: 
    
    """
    
    def __init__(self):
        super(self.__class__, self).__init__()
                    
    def cmeError(self, str):
        pat = "(.*) (\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))            
         
    def hostEEFiles(self, str):
        pat = "(\+SIFIXEV: Host EE Files Successfully Created)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
         
    def gpsacp(self, str):
        pat = "(AT\$GPSACP)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
         
    def gpssw(self, str):
        pat = "(AT\$GPSSW)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
    
    def sgact(self, str):
        pat = "(\#SGACT)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
                
    def fwSwitchOn(self, str):
        if "SYS user on" in str:
            self.fire_action(EventMsg(str, function_name()))
    
    def iccid(self, str):
        pat = "(\#CCID: )(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name(), matchObj.group(2)))
                

    

        
            
 