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
        
    def FwEnableTraces(self):
        self.enable_trace()
        self.enable_atflow()
    
    def simBtns(self):
        self.switchon()
        
    def onGsm(self):
        self.__uart.write("gpio 12 0")
        time.sleep(1)
        self.__uart.write("gpio 10 1")
        time.sleep(1)
        self.__uart.write("gpio 10 0")
        time.sleep(1)
        

class EventMsg():
    def __init__(self, line, event, str1=""):
        #uart line that has generate the event
        self.line=line
        #event name
        self.event=event
        #optional parameter
        self.str1 = str1
    
    def isErrorEvent(self):
        if self.event[-5:] == "Error":
            return True
        return False
    
    def isFaultEvent(self):
        if self.event[-6:] == "Failed":
            return True
        return False
    
    def isExcepton(self):
        if self.isFaultEvent() or self.isErrorEvent():
            return True
        return False
    
    def getExceptionType(self):
        #return xxxxxXXXXXX
        #evAtCmeError -> At
        if  self.isFaultEvent():
                return "Failed"
        if  self.isErrorEvent():
                return "Error"
        
    def getSource(self):
        #return xxXXxxx
        #evAtCmeError -> At
        return  self.event[2:4]
    
    def isAtEvent(self):
        if self.getSource() == "At" :
            return True
        return False
    
    def isFwEvent(self):
        if self.getSource() == "Fw" :
            return True
        return False
        
    def __str__(self):
        return "Event= " + self.event + " line= " + self.line 
     

class AutoEvents():
    """ 
    Events generates by state machine
    """
    def evFwAutoStuck(self, str):
        return (EventMsg(str, function_name()))
    def evAtAutoStuck(self, str):
        return (EventMsg(str, function_name()))
        

class ShellEvents(Observable, Parseble):
    
    def __init__(self):
        super(self.__class__, self).__init__()
                    
    def evAtCmeError(self, str):
        pat = "(.+) (\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))      
            return True
        return False   
    def evFwSysGpsStartupFailed(self, str):
        if "GPS configuration failed" in str:
            self.fire_action(EventMsg(str, function_name()))        
            return True
        return False
    
    def evFwSysGsmOnFailed(self, str):
        if "GSM status set ON failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False        
    def evFwSysGsmOFffFailed(self, str):
        if "GSM status set OFF failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False         
    def evAtHostEEFiles(self, str):
        if "SIFIXEV: Host EE Files Successfully Created" in str:
            self.fire_action(EventMsg(str, function_name()))                                             
            return True
        return False            
    def evFwSysStartupFailed(self, str):
        if "System startup failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False            
    def evFwSysNvmFailed(self, str):
        if "System NVM configuration failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False                            
    def evAtGpsacp(self, str):                        
        pat = "(AT\$GPSACP)(.*)"                
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False    
    def evAtSgactQuery(self, str):
        if "AT#SGACT" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False    
    def evAtSgactAns(self, str):
        if "#SGACT" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                #check it is an IP address
                ip_addr = splitted_txt[1].split('.')
                if len(ip_addr) == 4:
                    self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
                    return True
        return False                    
    def evFwGprsActFailed(self, str):
        if "System gprs connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evAtQueryProvisioning(self, str):
         if "AT#HTTPQRY=" in str and "provisioning" in str:
            self.fire_action(EventMsg(str, function_name()))   
            return True
         return False
        
    def evFwProvisioningFailed(self, str):
        if "System provisioning failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evAtRingOk(self, str):
        if "#HTTPRING: 0,200,\"text/plain;charset=UTF-8\"" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False    
        
    def evAtSsls(self, str):
        if "AT#SSLS=1" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evAtSsld(self, str):
        if "AT#SSLD" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwSystemTlsFailed(self, str):
        if "System tls connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
       
    def evFwMqttConnect(self, str):
        if "MQTT connect" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttConnectFailed(self, str):
        if "System mqtt connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttSusbscribedFailed(self, str):
        if "System mqtt subscribe failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evFwMqttHelloFailed(self, str):
        if "System mqtt hello failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttPubFailed(self, str):
        if "MQTT publish locations failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttPingFailed(self, str):
        if "MQTT ping failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False           
    
    def evFwSystemOnLine(self, str):
        if "System online" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
                
    def evAtCsq(self, str):
        if "+CSQ" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name()))     
                return True
        return False
            
    def evAtNoCarrier(self, str):
        if "NO CARRIER" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False

    def evFwButtonOnOff(self, str):
        if "BUTTON_MANAGER_EVENT_ONOFF received" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False            

                                
    def evFwSysUserOn(self, str):
        if "SYS user on" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwSysUseOff(self, str):
        if "SYS user off" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evFwOffline(self, str):
        if "System NOT online" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    
    def evAtGetIccid(self, str):
        if "#CCID" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
                return True
        return False
       
                 
    def evFwRecconnetInterval(self, str):
        if "Reconnect interval waiting" in str:
            splitted_txt = str.split( )
            timeout = splitted_txt[2]            
            self.fire_action(EventMsg(str, function_name(), timeout))
            return True
        return False
                       
                 

def test_ShellEvents():
    def test_print(ev):
        print "Found " + str(ev)
        
    sh = ShellEvents()
    sh.msubscribe(test_print)
    
    str = "AT#HTTPQRY=#0,0,\"/services/imhere/provisioning?iccid=89372021131119023740&firmware=140306093111"    
    #str = "Reconnect interval waiting"
    #str = " +CME ERROR: sss"
    #str = "#CCID  1 "
    str = "AT#SSLD=1,8883,54.204.45.147,1,1"

    sh.callAllFunc(str)

def test_IsSourceEvent():
    def test_(ev):
        print "Found " #+ str(ev)
        if (ev.isFwEvent()):
            print "Is Fw ev "
        if (ev.isAtEvent()):
            print "Is At ev "
        
    sh = ShellEvents()
    sh.msubscribe(test_)
    
    str = "AT#SSLD="
    #str = "Reconnect interval waiting"
    sh.callAllFunc(str)

if __name__ == "__main__":
    #test_ShellEvents()
    test_IsSourceEvent()
        
            
 