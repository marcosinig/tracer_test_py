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
                    
    def evCmeError(self, str):
        pat = "(.*) (\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))            
         
    def evHostEEFiles(self, str):
        if "SIFIXEV: Host EE Files Successfully Created" in str:
            self.fire_action(EventMsg(str, function_name()))
       
         
    def evGpsacp(self, str):
        pat = "(AT\$GPSACP)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
    
    def evSgactQuery(self, str):
        if "AT#SGACT" in str:
            self.fire_action(EventMsg(str, function_name()))
    
    def evSgactAns(self, str):
        if "#SGACT" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
     
    def evFwGprsActFailed(self, str):
        if "System gprs connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
                
    def evFwSwitchOn(self, str):
        if "SYS user on" in str:
            self.fire_action(EventMsg(str, function_name()))
    
    def evFwSwitchOff(self, str):
        if "SYS user off" in str:
            self.fire_action(EventMsg(str, function_name()))
    
    
    def evGetIccid(self, str):
        if "#CCID" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
            
                 

    

        
            
 