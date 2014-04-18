'''
Created on 14/apr/2014

@author: i'm Developer
'''

from imUtils  import *
from imCommands import *
 


class regHandlerConn(Parseble):
    """
    function names are called in base of shell and mqtt events
    
    """
    __log=1
    
    def __init__(self, clb):
        super(self.__class__, self).__init__()
        self._clb=clb
        
    def evFwSwitchOn(self, evt):
        if (self.__class__.__log):
            print "fwSwitchOn"
        self._clb(evt)
    def evFwReconnect(self, evt):
        if (self.__class__.__log):
            print "fwReconnect"
        self._clb(evt)
    def evGetIccid(self, evt):            
        if (self.__class__.__log):
            print "iccid " + evt.str1
        self._clb(evt)
    def evMqttHello(self, mqtMsgEvent):
        #action to be difened..!
        print "TestMqttEvents Hello"  
    def evFwGprsActFailed(self, evt):
        if (self.__class__.__log):
            print "evSgactFailed "  
        self._clb(evt)      
        pass
    def evSgactAns(self, mqtMsgEvent): 
        #print in log file
        
        #save      
        pass   
    def evSslErrors(self):
        #toimplement call
        
         #increment counter
         pass
    def evCmeErrors(self):
         
         #increment counter
         
         pass
    def evNoCarrier(self):
         
         #increment counter
         
         pass
    def evFwReconnection(self):
         #toimplement call (only first time)
         pass
    def evStatEndSession(self):
        #has to be called everytime the session expire
        
        #print total duration of session
        
        pass

class ConnectionProfiling(StateMachine):
    
    
    def start_state(self,ev):
        print function_name();
        if ev.event =="evFwSwitchOn":
            newState = "state_ON"
        return newState
    
    def on_state(self, ev):
        print function_name();
        if ev.event=="evGetIccid":
            newState = "state_connected"
        return newState
    
    def connected_state(self, ev):
        print function_name();
        if ev.event=="":
            newState = ""
        return newState

    def disconnected_state(self, ev):
        print function_name();
        if ev.event=="":
            newState = ""
        return newState


    def __init__(self):
        super(self.__class__, self).__init__()        
        self.evHand = regHandlerConn(self.run)
              
        self.add_state("Start", self.start_state)
        self.add_state("On", self.on_state)
        self.add_state("Connected", self.connected_state)
        self.add_state("Disconnected", self.disconnected_state)
     
     

    