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
    class State_Profiling():                
        def __init__(self):
            self.data = { 'numTimes':0, 'total_time':0, 'session_ts':None, 'session_min':0 }            
        
        def enter(self):               
            self.data['session_ts'] = myTime.getTimestamp()
            self.data['numTimes'] += 1 
            #self._log.info("online times " + str(self.online_nt)) 
        
        def exit(self):
            if self.data['session_ts'] != None:
                self.data['session_min'] = myTime.getDiffNowMin( self.session_t  )
                self.data['total_time'] +=  self.data['session_min']
        
        def __str__(self):
            line = """ Status " + self.__class__.__name__ + " 
                    has last session duration minutes " + self.session_tm
    
    class Online_p (State_Profiling):
        pass 
            
    def __init__(self, logEv):
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.logEv = logEv

        self.eventsProf = []
        
        self.iccid = None
        self.ip = None
        
        #statistic on device, calculated as the amount of time that is not on the off state
        self.on_session_t = None
        self.on_total_t = 0
        
        #startistics disconnected, updated everytime enter/exit disconnected status
        self.disconnected_nt = -1
        
        #statistics online, update in on_line status
        self.online_nt=0 
        self.online_total_t = 0
        self.online_session_t = None
        
        self.gprs_nt=0
        self.gprs_total_t = 0
        self.gprs_session_t = None
        
        self.gprs_nt=0
        self.gprs_total_t = 0
        self.gprs_session_t = None
        
        self.provisioning_nt=0
        self.provisioning_total_t = 0
        self.provisioning_session_t = None

        self.ssl_nt=0
        self.ssl_total_t = 0
        self.ssl_session_t = None
        
        self.mqtt_nt=0
        self.mqtt_total_t = 0
        self.mqtt_session_t = None        
    
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
       
        self.disconnected_nt += 1 
        self._log.info("Disconnected times " + str(self.disconnected_nt)) 
        
        if self.disconnected_nt == 1 :
            #print minutes_on_line_session online_total_t disconnected_nt
            profEv = ConnProfileEv(myTime.getTimestamp(), "State Disconnected", ev)
            self.attachEv(profEv)
                    
    def disconnected_exit(self, ev):        
        pass                                                                 
        
    
    def online_enter(self, ev):
        self._log.info(function_name())   
        self.online_session_t = myTime.getTimestamp()
        self.online_nt += 1 
        self._log.info("online times " + str(self.online_nt)) 
                
        profEv = ConnProfileEv(myTime.getTimestamp(), "Connected Data", ev)
        self.attachEv(profEv)
    
    def online_exit(self, ev):
        self._log.info(function_name())   
        #WARN: is this necessary?!?!?
        if self.online_session_t != None:
            minutes = myTime.getDiffNowMin( self.online_session_t  )
            self.online_total_t += minutes
            
            profEv = ConnProfileEv(myTime.getTimestamp(), "Exiting Online", ev)
            self.attachEv(profEv) 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total minutes Session Connection=" + str(minutes) )
            self._log.info( "Total Overall Connection=" + str(self.online_total_t) )  
        
            self.logEv("Total minutes Session Connection=" + str(minutes))
            self.logEv("Total Overall Connection=" + str(self.online_total_t)) 
            
            self.online_session_t = None 
   
    def gprs_enter(self, ev):
        self._log.info(function_name())
        self.gprs_session_t = myTime.getTimestamp()
        self.gprs_nt += 1 
        self._log.info("gprs_nt times " + str(self.gprs_nt)) 
                
        profEv = ConnProfileEv(myTime.getTimestamp(), "Trying gprs", ev) 
    
    def gprs_exit(self, ev):
        self._log.info(function_name())   
        #WARN: is this necessary?!?!?
        if self.gprs_session_t != None:
            minutes = myTime.getDiffNowMin( self.gprs_session_t  )
            self.gprs_total_t += minutes
            
            profEv = ConnProfileEv(myTime.getTimestamp(), "Exiting Gprs", ev)
            self.attachEv(profEv) 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total gprs Session Connection=" + str(minutes) )
            self._log.info( "Total gprs Connection=" + str(self.gprs_total_t) )  
        
            self.logEv("Total gprs Session Connection=" + str(minutes))
            self.logEv("Total gprs Connection=" + str(self.gprs_total_t)) 
            
            self.gprs_session_t = None     
         
    def provisioning_enter(self, ev):
        self._log.info(function_name())
        self.provisioning_session_t = myTime.getTimestamp()
        self.provisioning_nt += 1 
        self._log.info("provisioning_nt times " + str(self.provisioning_nt)) 
                
        profEv = ConnProfileEv(myTime.getTimestamp(), "Entering provisioning", ev) 
    
    def provisioning_exit(self, ev):
        self._log.info(function_name())   
        #WARN: is this necessary?!?!?
        if self.provisioning_session_t != None:
            minutes = myTime.getDiffNowMin( self.provisioning_session_t  )
            self.provisioning_total_t += minutes
            
            profEv = ConnProfileEv(myTime.getTimestamp(), "Exiting provisioning", ev)
            self.attachEv(profEv) 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total provisioning Session Connection=" + str(minutes) )
            self._log.info( "Total provisioning Connection=" + str(self.provisioning_total_t) )  
        
            self.logEv("Total provisioning Session Connection=" + str(minutes))
            self.logEv("Total provisioning Connection=" + str(self.provisioning_total_t)) 
            
            self.gprs_session_t = None 
            
    def ssl_enter(self, ev):
        self._log.info(function_name())
        self.ssl_session_t = myTime.getTimestamp()
        self.ssl_nt += 1 
        self._log.info("ssl_nt times " + str(self.ssl_nt)) 
                
        profEv = ConnProfileEv(myTime.getTimestamp(), "Entering ssl", ev)
    
    def ssl_exit(self, ev):
        self._log.info(function_name())   
        #WARN: is this necessary?!?!?
        if self.ssl_session_t != None:
            minutes = myTime.getDiffNowMin( self.ssl_session_t  )
            self.ssl_total_t += minutes
            
            profEv = ConnProfileEv(myTime.getTimestamp(), "Exiting ssl", ev)
            self.attachEv(profEv) 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total ssl Session Connection=" + str(minutes) )
            self._log.info( "Total ssl Connection=" + str(self.ssl_total_t) )  
        
            self.logEv("Total ssl Session Connection=" + str(minutes))
            self.logEv("Total ssl Connection=" + str(self.ssl_total_t)) 
            
            self.ssl_session_t = None  
    
    def mqttConn_enter(self, ev):
        self._log.info(function_name())
        self.mqtt_session_t = myTime.getTimestamp()
        self.mqtt_nt += 1 
        self._log.info("mqtt_nt times " + str(self.mqtt_nt)) 
                
        profEv = ConnProfileEv(myTime.getTimestamp(), "Entering mqtt", ev) 
    
    def mqttConn_exit(self, ev):
        self._log.info(function_name())   
        #WARN: is this necessary?!?!?
        if self.mqtt_session_t != None:
            minutes = myTime.getDiffNowMin( self.mqtt_session_t  )
            self.mqtt_total_t += minutes
            
            profEv = ConnProfileEv(myTime.getTimestamp(), "Exiting mqtt", ev)
            self.attachEv(profEv) 
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
            self._log.info( "Total mqtt Session Connection=" + str(minutes) )
            self._log.info( "Total mqtt Connection=" + str(self.mqtt_total_t) )  
        
            self.logEv("Total mqtt Session Connection=" + str(minutes))
            self.logEv("Total mqtt Connection=" + str(self.mqtt_total_t))  
            
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
        self._log.info( "Total Overall Connection=" + str(self.online_total_t) )



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
             
           
      
