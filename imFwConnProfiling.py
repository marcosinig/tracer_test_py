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
    def __init__(self, timestamp, msg, event):
        self.timestamp = timestamp
        self.msg = msg
        self.event = event
    
    def __str__(self):
        return self.timestamp + "-" + self.msg + "-" + self.event
        

class ConnProfiling():
    
    def __init__(self, logEv):
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.logEv = logEv

        self.eventsProf = []
        
        self.iccid = None
        self.ip = None
        
        self.on_session = None
        self.on_total = 0
        
        self.gprs_on_ntimes=0        
        self.disconnected_ntimes=0
        
        self.connected_total = 0
        self.connected_session=0
    
    
    def go_off(self, ev):
        self.on_total = myTime.getDiffNowMin( self.on_session  )
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Switching off", ev)
        self.attachEv(profEv)
    
    def go_disconnected(self, ev):    
        
        if self.on_session == 0:
            #it now on, tarck it
            self.on_session = myTime.getTimestamp()        
            profEv = ConnProfileEv(myTime.getTimestamp(), "Switched On", ev)
            self.attachEv(profEv)
            
        minutes_session = myTime.getDiffNowMin( self.connected_session  )
        self.connected_total += minutes_session 
        self.disconnected_ntimes += 1 
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Disconnected data", ev)
        self.attachEv(profEv)
        
        #THIS DATA HAS TO BE PRINTED ONLY IF WE WERE CONNECTED...!
        self._log.info( "Total minutes Session Connection=" + str(minutes_session) )
        self._log.info( "Total Overall Connection=" + str(self.connected_total) )  
        
        self.logEv("Total minutes Session Connection=" + str(minutes_session))
        self.logEv("Total Overall Connection=" + str(self.connected_total))     
        
    def go_try_gprs(self, ev):
        pass
    
    
    def go_gprs_on(self, ev):
        self.gprs_on_ntimes += 1 
        self._log.info("Connected times " + str(self.gprs_on_ntimes)) 
        self.connected_session = myTime.getTimestamp()
        
        profEv = ConnProfileEv(myTime.getTimestamp(), "Connected Data", ev)
        self.attachEv(profEv)
    
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
        self._log.info( "Total Overall Connection=" + str(self.connected_total) )


class FwConnStateMachine(StateMachine):
        
    def off_state(self,ev):
<<<<<<< HEAD
        newState = None        
        self._log.info(function_name())
=======
        newState = None
>>>>>>> branch 'master' of https://github.com/marcosinig/tracer_test_py.git
        
               
        if ev.event == "evFwSysGsmOnFailed":
            pass
        
<<<<<<< HEAD
        if ev.event == "evFwSysUserOn":
=======
        return newState    
    
    def on_state(self, ev):
        newState = None
                
        if ev.event=="evAtGetIccid":
            self.iccid = ev.str1
        if ev.event == "evAtSgactAns":
            self.ip =  ev.str1
            newState = "Connected"
            self.actionGoToConntected()
        
        
        return newState
    
    def connected_state(self, ev):
        newState = None
                        
        
        if ev.event=="evAtNoCarrier" or ev.event=="evFwOffline" or  ev.event=="evFwRecconnetInterval":
>>>>>>> branch 'master' of https://github.com/marcosinig/tracer_test_py.git
            newState = "disconnected"
            #self.rcv_evFwSwitchOn = True            

        #evAtHostEEFiles has to be managed
            
        #if ev.event == "evAtHostEEFiles" and self.rcv_evFwSwitchOn:
        #    newState = "disconnected"
            #should go in sys setup...
            #self.connProf.go_disconnected(ev)   
        
        return newState
    

    def disconnected_state(self, ev):
        newState = None
<<<<<<< HEAD
        self._log.info(function_name())
=======
>>>>>>> branch 'master' of https://github.com/marcosinig/tracer_test_py.git
        
        #this should be handled in sys setup state
        if ev.event== "evFwSysGpsStartupFailed" or ev.event=="evFwSysNvmFailed" or ev.event=="evFwSysStartupFailed":  
            #raise error
            #WHAT IS HAPPENING? 
            pass
        
        #FW HAS TO GO OFF FOR ERRORS; HOW?
        
        if ev.event=="evAtGetIccid":
            self.connProf.set_iccid(ev.str1)
       
        if ev.event == "evAtSgactQuery":
            newState= "try_gprs"
            #self.connProf.go_try_gprs()                            
        
        if ev.event=="evFwSysUseOff":
            newState = "off"
            self.init_off()
            self.connProf.go_off(ev)  
                                
        return newState
    
    def try_gprs_state(self, ev):
        newState = None
        self._log.info(function_name())

        
        if ev.event == "evAtSgactAns":
            self.connProf.set_ip(ev.str1)
        
        if ev.event == "evAtCmeError":
            self.connProf.ev_cme_error()
        
        #WARN: Should move on with the evAtSgactAns!
        if ev.event == "evAtQueryProvisioning":  
            newState = "try_provisioning" 
        
        if ev.event == "evFwGprsActFailed":
            newState = "disconnected"
        
        return newState
    
    def try_provosioning_state(self, ev):
        newState = None
        self._log.info(function_name())

        if ev.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                                    
        if ev.event == "evFwProvisioningFailed":
            newState = "disconnected"             
                    
        if ev.event == "evAtRingOk":
            newState = "try_ssl"   
            #WARN: should move on with the answer
        
        return newState
    
    def try_ssl_state(self, ev):
        newState = None
        self._log.info(function_name())

        if ev.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                              
        if ev.event == "evFwSystemTlsFailed":
            newState = "disconnected" 
                    
        if ev.event == "evFwMqttConnect":
            newState = "try_mqttConn"   
        
        return newState
<<<<<<< HEAD

    def try_mqttConn_state(self, ev):                 
        newState = None
        self._log.info(function_name())               

        if ev.event == "evAtCmeError":
            self.connProf.ev_cme_error()
                    
        if ev.event == "evFwMqttConnectFailed":
            newState = "disconnected" 

        if ev.event == "evFwMqttPubFailed":
            #raise error
            pass
                    
        if ev.event == "evFwSystemOnLine":
            newState = "on_line"   
            self.connProf.go_gprs_on(ev)
        
        return newState
    
    def on_line_state(self, ev):
        newState = None
        self._log.info(function_name())               

        if ev.event == "evAtCmeError":
            self.connProf.ev_cme_error()

        if ev.event == "evFwMqttPubFailed" or ev.event == "evFwMqttPIngFailed":
            #raise error
            pass 

                    
        if ev.event=="evFwRecconnetInterval":
            newState = "disconnected"
            #self.connProf.go_disconnected(ev)   
        
        if ev.event=="evFwSysUseOff":
            newState = "off"
            self.init_off()            
                            
        return newState
=======
>>>>>>> branch 'master' of https://github.com/marcosinig/tracer_test_py.git

    def stuck_state(self, ev):
        #TODO: implement this state when fw is stuck
        pass    

    def init_off(self):
        self.rcv_evFwSwitchOn= False

    def __init__(self, connProfiling, logEv):
        super(self.__class__, self).__init__()
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
                
        self.evHand = regHandlerConn(self.run, self, logEv)        
        self.connProf = connProfiling                        
                      
        self.add_state("Off", self.off_state)
        self.set_start("Off")
        
        self.add_state("on_line", self.on_line_state)
        self.add_state("Disconnected", self.disconnected_state)
        
        self.add_state("try_provisioning", self.try_provosioning_state)
        self.add_state("try_ssl", self.try_ssl_state)
        self.add_state("try_mqttConn", self.try_mqttConn_state)
        self.add_state("try_gprs", self.try_gprs_state)                                        
        
        #unkown state
        self.add_state("stuck", self.stuck_state)
        
        #has to be removed
        self.init_off()
       
     
     

    
