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
    def __init__(self, timestamp, msg, obj):
        #obj has to implement to string
        
        self.timestamp = timestamp
        self.msg = msg
        self.obj = obj
    
    def __str__(self):
        return self.timestamp + "-" + self.msg + "-" + self.obj
        
class ProfReport():
    #TODO add dynamiclly data field
    def __init__(self, report):
        self.report = report
    

class ConnProfiling():
    
    def __init__(self, logEv):
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.logEv = logEv

        self.eventsProf = []
        
        self.iccid = None
        self.ip = None
        
        #statistic on device
        self.sw_on_session = None
        self.sw_on_total = 0
        
        #startistics disconnected
        self.disconnected_ntimes = -1
        
        #statistics online
        self.online_ntimes=0 
        self.online_total = 0
        self.online_session = None
    
    
    def off_enter(self, ev): 
        self._log.info(function_name())
        
        if self.sw_on_session != None:
            self.sw_on_total = myTime.getDiffNowMin( self.sw_on_session  )        
            #print sw_on_total and sw_on_session
            pass
            profEv = ConnProfileEv(myTime.getTimestamp(), "Switching off", ev)
            self.attachEv(profEv)
    
            self.sw_on_session = None
    
                                    
    def off_exit(self, ev):
        self._log.info(function_name())         
        self.sw_on_session = myTime.getTimestamp()        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Switched On", ev)
        self.attachEv(profEv)
    
    
    def disconnected_enter(self, ev):  
        self._log.info(function_name())   
       
        self.disconnected_ntimes += 1 
        
        if self.disconnected_ntimes == 1 :
            #print minutes_on_line_session online_total disconnected_ntimes
            profEv = ConnProfileEv(myTime.getTimestamp(), "State Disconnected", ev)
            self.attachEv(profEv)
        
            report = ""
            #TODO: write report
            self.attachEv( ProfReport(report) )
        
            
        
        self.online_session = None 
        
    def exit_disconnected(self):
        
        pass                                                                 
        
    
    def enter_online(self, ev):
        self.online += 1 
        self._log.info("Connected times " + str(self.gprs_on_ntimes)) 
        self.online_session = myTime.getTimestamp()
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Connected Data", ev)
        self.attachEv(profEv)
    
    def exit_online(self, ev):
        if self.online_session != None:
            minutes_on_line_session = myTime.getDiffNowMin( self.online_session  )
            self.online_total += minutes_on_line_session 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total minutes Session Connection=" + str(minutes_on_line_session) )
            self._log.info( "Total Overall Connection=" + str(self.online_total) )  
        
            self.logEv("Total minutes Session Connection=" + str(minutes_on_line_session))
            self.logEv("Total Overall Connection=" + str(self.online_total))    
        
    
    def ev_cme_error(self, state, ev):
        self._log.info("Cme Error in state " + state + "ev: " + ev)
                                

    def set_iccid(self, iccid):
        self.iccid=iccid
    def set_ip(self, ip):
        self.ip = ip
    def attachEv(self, connProfileEv):
        self.eventsProf.append(connProfileEv)  
    
    def printEvents(self):
        pass
    
    def printReport(self):
        self._log.info("Connected times " + str(self.gprs_on_ntimes))
        self._log.info("Disconnected times " + str(self.gprs_on_ntimes))
        self._log.info( "Total Overall Connection=" + str(self.online_total) )



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
            newState = "Disconnected_state" 

        if event.event == "evFwMqttPubFailed":
            #raise error
            pass
                    
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
            #self.connProf.go_disconnected(ev)   
        
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
             
           
      
