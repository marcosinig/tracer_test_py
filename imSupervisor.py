'''
Created on 14/apr/2014

@author: i'm Developer

TODO:

-passare handler al file di log!

- print statistic info to file e ??
- comando per scatenare il ping statistiche
- fare classe Profiling con solo dati prof

-CSQ keep alive -> se manca perso connessione..!


Verificare:
- date

Improvements:
- L'handler degli eventi deve sottoscrivere e non usare parsable (problema eventi non esistenti)
- State machine non � il max 


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
            print function_name()
        self._clb(evt)
  
    def evAtGetIccid(self, evt):            
        if (self.__class__.__log):
            print function_name() + " iccid " + evt.str1
        self._clb(evt)
    def evMqttHello(self, mqtMsgEvent):
        print function_name() +" TestMqttEvents Hello"  
    def evFwGprsActFailed(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt) 
        
    #connected event         
    def evAtSgactAns(self, evt): 
        if (self.__class__.__log):
            print function_name()  
        self._clb(evt)   
 
    #general errors
    def evAtCmeError(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt)  
    
    def evAtCsq(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt)
        
    #disconnect events
    def evFwSystemReconnect(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt)          
    def evFwOffline(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt)
    def evAtNoCarrier(self, evt):
        if (self.__class__.__log):
            print function_name()           
        self._clb(evt)  
    def evFwRecconnetInterval(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt)  
    def evAtSslErrors(self, evt):
        if (self.__class__.__log):
            print function_name() 
        self._clb(evt) 
        
   
         
def getTimestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getMinutes(dt):
    return dt.seconds/60

class ConnectionProfiling(StateMachine):
        
    def off_state(self,ev):
        newState = None
        print function_name();
        
        if ev.event =="evFwSwitchOn":            
            newState = "On"
        
        if self.on_session != 0:
            self.on_total += getTimestamp() - self.on_session
        
        if newState != None:
            print "new State: " + newState 
        return newState    
    
    def on_state(self, ev):
        newState = None
        print function_name();
        
        on_session = getTimestamp()
        
        if ev.event=="evAtGetIccid":
            self.iccid = ev.str1
        if ev.event == "evAtSgactAns":
            self.ip =  ev.str1
            newState = "Connected"
        
        if newState != None:
            print "new State: " + newState
        return newState
    
    def connected_state(self, ev):
        newState = None
        print function_name();
        
        self.connected_session = getTimestamp()
        
        
        if ev.event=="evAtNoCarrier" or ev.event=="evFwOffline" or  ev.event=="evFwRecconnetInterval":
            newState = "disconnected"
        
        #if ev.event=="evFwSwitchOff":
        #    newState = "off"    
        
        if newState != None:
            print "new State: " + newState
        return newState

    def disconnected_state(self, ev):
        newState = None
        print function_name();
        
        self.connected_total += getTimestamp() - self.connected_session
        print "Total Session Connection=" + getMinutes(self.connected_session)
        print "Total Overall Connection=" + getMinutes(self.connected_total)
        
        
        #if ev.event=="evFwSwitchOff":
        #    newState = "off"
        
        if newState != None:
            print "new State: " + newState
        return newState

    

    def __init__(self):
        super(self.__class__, self).__init__()        
        self.evHand = regHandlerConn(self.run)
        
        self.iccid=None
        self.ip=None
        
        self.on_session=0
        self.on_total=0
        
        self.connected_session=0
        self.connected_total=0
              
        self.add_state("Off", self.off_state)
        self.set_start("Off")
        
        self.add_state("On", self.on_state)
        self.add_state("Connected", self.connected_state)
        self.add_state("Disconnected", self.disconnected_state)
        
        #unkown state
        self.add_state("Unkown", self.unkown_state)
       
     
     

    