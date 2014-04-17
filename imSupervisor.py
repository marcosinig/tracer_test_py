'''
Created on 14/apr/2014

@author: i'm Developer
'''

from imUtils  import *
from imCommands import *


class Statistics(Parseble):
    """
    function names are called in base of shell and mqtt events
    
    """
    __log=1
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self._fwSwitchesOn=0
    
    def fwSwitchOn(self, evt):
        if (Statistics.__log):
            print "fwSwitchOn"
            
    def fwReconnect(self, evt):
        if (Statistics.__log):
            print "fwReconnect"

    def getIccid(self, evt):            
        if (Statistics.__log):
            print "iccid " + evt.str1 
    
    def mqttHello(self, mqtMsgEvent):
        #action to be difened..!
        print "TestMqttEvents Hello"  
        
        
    def sgactFailed(self, mqtMsgEvent):
        #toimplement call
        
        #increment failed activation
        
        pass
    
    def sgactSessionFailed(self):
        #toimplement call
        
        #print into log
        
        #increment counter failed sessions
        pass

        
    def sgactAns(self, mqtMsgEvent): 
        #print in log file
        
        #save      
        pass   
    
    def sslErrors(self):
        #toimplement call
        
         #increment counter
         pass

    def cmeErrors(self):
         
         #increment counter
         
         pass
     
    def noCarrier(self):
         
         #increment counter
         
         pass
     
    def fwReconnection(self):
         #toimplement call (only first time)
         pass
     
     
    def StatEndSession(self):
        #has to be called everytime the session expire
        
        #print total duration of session
        
        pass



class MonitorConnections():
    