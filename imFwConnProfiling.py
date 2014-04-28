'''
Created on 14/apr/2014

@author: i'm Developer

TODO:

- venet deve avere accesso a profiling e non logEv!!!!!

-cambiare macchina a stati sugli eventi? logica piu chiara.

-CSQ keep alive -> se manca perso connessione..!


Verificare:

Improvements:
- L'handler degli eventi deve sottoscrivere e non usare parsable (problema eventi non esistenti)
- State machine non e il max 


'''

from imUtils  import *
from imFwInterface import *
from imStateMachine import *
import logging
import copy

#SHOULD NOT BE USED
#HAS TO BE INVESTIGATED
logger = logging.getLogger(__name__)        
configureLog(logger)


class regHandlerConn(Parseble):
    """
    function names are called in base of shell and mqtt events
    
    """
    __log=1
    
    def __init__(self, clb, stateMachine, logEv):
        super(self.__class__, self).__init__()
        self._clb=clb
        self.stateM = stateMachine
        self.logEv= logEv
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def evFwSysUserOn(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)
        
    def evFwSysUseOff(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)
        
    #def evFwButtonOnOff(self, evt):
    #    if (self.__class__.__log):
    #        self._log.debug( function_name() )
    #    self._clb(evt)
    
    #***
    def evFwSysGsmOnFailed(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)
    
    
    #def evFwSysGsmOFffFailed(self, evt):        
    #    if (self.__class__.__log):
    #        self._log.debug( function_name() )
    #    self._clb(evt)
       
    def evFwSysGpsStartupFailed(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)

    def evFwSysNvmFailed(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)    

    def evFwSysStartupFailed(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)     
                              
    def evAtGetIccid(self, evt):            
        if (self.__class__.__log):
            self._log.debug( function_name() + " iccid " + evt.str1 )
        self._clb(evt)
        
    def evFwGprsActFailed(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name())
        self._clb(evt) 
        
    #GPRS event         
    def evAtSgactQuery(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt)
        
    def evAtSgactAns(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
    
    #provisioning
    def evAtQueryProvisioning(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
    
    def evFwProvisioningFailed(self, evt):
         if (self.__class__.__log):
            self._log.debug( function_name()  )
         self._clb(evt)
    
    def evAtRingOk(self, evt):
         if (self.__class__.__log):
            self._log.debug( function_name()  )
         self._clb(evt)
    
    def evFwMqttConnect(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt)
         
    def evAtSsld(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
        
    def evFwSystemTlsFailed(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
    
    def evFwMqttSusbscribedFailed(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
    
    def evFwMqttHelloFailed(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
        
    def evFwMqttPubFailed(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
                
    def evFwMqttPingFailed(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt)        
                        
    def evFwSystemOnLine(self, evt): 
        if (self.__class__.__log):
            self._log.debug( function_name()  )
        self._clb(evt) 
 
    #general errors
    def evAtCmeError(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )    
        self._log.error( function_name() + str(evt))        
        self._clb(evt)  
    
    def evAtHostEEFiles(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )                   
        self._clb(evt)  
    
    #CSQ - not used..
    def evAtCsq(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )  
        #if self.stateM == "Connected".upper():
        #    pass           
        #self._clb(evt)
    
    #reconnect procedure, NOT HANDLED yet    
    def evFwSystemReconnect(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)    
    
    #disconnect events      
    def evFwOffline(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)
    def evAtNoCarrier(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )  
        self._log.error( function_name() + str(evt))                
        self._clb(evt)  
    def evFwRecconnetInterval(self, evt):
        if (self.__class__.__log):
            self._log.debug( function_name() )
        self._clb(evt)  
        
class ConnProfileEv():
    def __init__(self, timestamp, msg, ev, status_p = None, error_ev = None):
        #obj has to implement to string
        
        self.timestamp = timestamp
        self.msg = msg
        self.ev = ev
        #status report
        self.status_p = status_p
        #list of all the possible errors
        self.error_ev = error_ev
    
    def __str__(self):
        #TODO write in base of what is present in nice way
        line = str( self.timestamp ) + " - " + self.msg + " - \n\t" + str(self.ev)
        if self.status_p != None:
            line += "- \t" + str(self.status_p)
        if self.error_ev != None:
            line += "- \n\t"
            for errL in self.error_ev:
                line += str( errL )        
        return line 
    

class ConnProfiling():
    class State_Profiling():                
        def __init__(self, stateName):
            self.data = { 'state_Name': stateName,'numTimes':0, 'total_time':0, 'session_ts':None, 'session_min':0 }            
        
        def enter(self):               
            self.data['session_ts'] = myTime.getTimestamp()
            self.data['numTimes'] += 1 
            return  self.data['numTimes']
        
        def exit(self):
            if self.data['session_ts'] != None:
                self.data['session_min'] = myTime.getDiffNowMin( self.data['session_ts']  )
                self.data['total_time'] +=  self.data['session_min']
                self.data['session_ts'] = None
        
        def __str__(self):
            line1 = "State {state_Name} last session duration min {session_min} overall durations min {total_time} activated ntimes {numTimes}"
            return line1.format(**self.data)
            
    def __init__(self, logEv):
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.logEv = logEv
        
        #list of all the events reported by the profile class
        self.eventsProf = []
        #list of all the errors, it has to be empty everytime a state is exited
        self.eventsError = []
        
        self.iccid = None
        self.ip = None
        
        #statistic on device, calculated as the amount of time that is not on the off state
        self.on_session_t = None
        self.on_total_t = 0
        
        #startistics disconnected, updated everytime enter/exit disconnected status
        self.disconnected_nt = -1
        
        self.online_p = ConnProfiling.State_Profiling("Online")
        self.disconnected_p = ConnProfiling.State_Profiling("Disconnected")
        self.gprs_p = ConnProfiling.State_Profiling("Gprs")
        self.provisioning_p = ConnProfiling.State_Profiling("Provisioning")
        self.ssl_p = ConnProfiling.State_Profiling("Ssl")
        self.mqtt_p = ConnProfiling.State_Profiling("Mqtt")
               
    
    def off_enter(self, ev): 
        self._log.info(function_name())
        
        if self.on_session_t != None:
            self.on_total_t = myTime.getDiffNowMin( self.on_session_t  )        
            #print on_total_t and on_session_t
            pass
            profEv = ConnProfileEv(myTime.getTimestamp(), "Switching off", ev)
            self.attachEv(profEv)
    
            self.on_session_t = None
    
                                    
    def off_exit(self, ev):
        self._log.info(function_name())         
        self.on_session_t = myTime.getTimestamp()        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Switched On", ev)
        self.attachEv(profEv)
    
    
    def disconnected_enter(self, ev):  
        self._log.info(function_name())   
       
        self.disconnected_p.enter()
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "State Disconnected", ev)
        self.attachEv(profEv)
                    
    def disconnected_exit(self, ev):        
        pass                                                                 
        
    
    def online_enter(self, ev):
        self._log.info(function_name())   
        
        self.disconnected_p.exit()
        profEv = ConnProfileEv(myTime.getTimestamp(), "Disconnected Exit", ev, copy.deepcopy(self.disconnected_p))
        self.attachEv(profEv) 
        
        self.online_p.enter()
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Online Enter", ev)
        self.attachEv(profEv)
    
    def online_exit(self, ev):
        self._log.info(function_name())   
        
        self.online_p.exit()
        #self._log.info(str (self.online_p) )
        #copy_p = copy.deepcopy(self.online_p)
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Online Exit", ev, copy.deepcopy(self.online_p))
        self.attachEv(profEv) 
   
    def gprs_enter(self, ev):
        self._log.info(function_name())
        
        self.gprs_p.enter()

        profEv = ConnProfileEv(myTime.getTimestamp(), "Gprs enter", ev) 
        self.attachEv(profEv)
    
    def gprs_exit(self, ev):
        self._log.info(function_name())   
        
        self.gprs_p.exit()
        #self._log.info(str (self.gprs_p) )
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Gprs exit", ev, copy.deepcopy(self.gprs_p)) 
        self.attachEv(profEv)
         
    def provisioning_enter(self, ev):
        self._log.info(function_name())
       
        self.provisioning_p.enter()

        profEv = ConnProfileEv(myTime.getTimestamp(), "Provisioning enter", ev) 
        self.attachEv(profEv)
    
    def provisioning_exit(self, ev):
        self._log.info(function_name()) 
          
        self.provisioning_p.exit()
        self._log.info(str (self.provisioning_p) )
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Provisioning exit", ev, copy.deepcopy(self.provisioning_p)) 
        self.attachEv(profEv)
            
    def ssl_enter(self, ev):
        self._log.info(function_name())
       
        self.ssl_p.enter()

        profEv = ConnProfileEv(myTime.getTimestamp(), "Ssl enter", ev) 
        self.attachEv(profEv)
    
    def ssl_exit(self, ev):
        self._log.info(function_name())   
          
        self.ssl_p.exit()
        self._log.info(str (self.ssl_p) )
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Ssl exit", ev, copy.deepcopy(self.ssl_p)) 
        self.attachEv(profEv)
    
    def mqttConn_enter(self, ev):
        self._log.info(function_name())
        
        self.mqtt_p.enter()

        profEv = ConnProfileEv(myTime.getTimestamp(), "Mqtt enter", ev) 
        self.attachEv(profEv)
    
    def mqttConn_exit(self, ev):
        self._log.info(function_name())  
         
        self.mqtt_p.exit()
        self._log.info(str (self.mqtt_p) )
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Mqtt exit", ev, copy.deepcopy(self.mqtt_p)) 
        self.attachEv(profEv) 
            
    def ev_cme_error(self, state, ev):
        self._log.info("Cme Error in state " + state + "ev: " + ev)
                                
    def set_iccid(self, iccid):
        self.iccid=iccid
    def set_ip(self, ip):
        self.ip = ip
    def attachEv(self, ev):
        self.eventsProf.append(ev)  
        self._log.info(ev)
    
    def printEvents(self):
        pass
    
    def printReport(self):
        pass



class Off_state(StateFath):
    
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        self.startState = True 
        
    def processEv(self, event):
        newState = None

        if event.event == "evFwSysGsmOnFailed":
            pass
        
        if event.event == "evFwSysUserOn":
            newState = "Disconnected_state"
        
        return newState   

class Disconnected_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def processEv(self, event):
        newState = None
        
        if event.event== "evFwSysGpsStartupFailed" or event.event=="evFwSysNvmFailed" or event.event=="evFwSysStartupFailed":  
            #raise error
            #WHAT IS HAPPENING? 
            pass
        
        #FW HAS TO GO OFF FOR ERRORS; HOW?
        
        #if event.event=="evAtGetIccid":
        #    self.connProf.set_iccid(event.str1)
       
        if event.event == "evAtSgactQuery":
            newState= "Gprs_state"
            #self.connProf.go_try_gprs()                            
        
        if event.event=="evFwSysUseOff":
            newState = "Off_state"
            self.init_off()
            self.connProf.go_off(event)   
                
        return newState   

class Gprs_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        #if event.event == "evAtSgactAns":
        #    self.connProf.set_ip(event.str1)
        
        if event.event == "evAtCmeError":
            self.connProf.ev_cme_error()
        
        #WARN: Should move on with the evAtSgactAns!
        if event.event == "evAtQueryProvisioning":  
            newState = "Provosioning_state" 
        
        if event.event == "evFwGprsActFailed":
            pass
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
        
        return newState
    
class Provosioning_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                                    
        if event.event == "evFwProvisioningFailed":
            pass         
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evAtRingOk":
            newState = "Ssl_state"   
            #WARN: should move on with the answer
        
        return newState

class Ssl_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                              
        if event.event == "evFwSystemTlsFailed":
            pass
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evFwMqttConnect":
            newState = "MqttConn_state"   
        
        return newState

class MqttConn_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def processEv(self, event):
        newState = None

        if event.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                    
        if event.event == "evFwMqttConnectFailed":
            pass 

        if event.event == "evFwMqttPubFailed":
            #raise error
            pass
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state"        
                    
        if event.event == "evFwSystemOnLine":
            newState = "Online_state"   
            #self.connProf.go_gprs_on(event)
        
        return newState

class Online_state(StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.event == "evAtCmeError":
            self.connProf.ev_cme_error()

        if event.event == "evFwMqttPubFailed" or event.event == "evFwMqttPIngFailed":
            #raise error
            pass 
                    
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state"
        
        if event.event=="evFwSysUseOff":
            newState = "off_state"
            self.init_off()            
            
        return newState

class FactryStateMachine():
    def __init__(self, connProfiling, logEv):
        
        sm = StateMachine()
        
        self.evHand = regHandlerConn(sm.process, self, logEv)        
        self.connProf = connProfiling      
        
        
        sm.add_state(Off_state(self.connProf))
        sm.add_state(Disconnected_state(self.connProf))
        sm.add_state(Gprs_state(self.connProf))
        sm.add_state(Provosioning_state(self.connProf))
        sm.add_state(Ssl_state(self.connProf))
        sm.add_state(MqttConn_state(self.connProf))
        sm.add_state(Online_state(self.connProf))
             
           
      
