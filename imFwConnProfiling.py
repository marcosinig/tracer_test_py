'''
Created on 14/apr/2014

@author: i'm Developer

TODO:

-cambiare macchina a stati sugli eventi? logica piu chiara.

- comando per scatenare il ping statistiche
- fare classe Profiling con solo dati prof

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
    
    def __init__(self, clb):
        super(self.__class__, self).__init__()
        self._clb=clb
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def evFwSwitchOn(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )
        self._clb(evt)
  
    def evAtGetIccid(self, evt):            
        if (self.__class__.__log):
            self.logger.debug( function_name() + " iccid " + evt.str1 )
        self._clb(evt)
        
    def evFwGprsActFailed(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name())
        self._clb(evt) 
        
    #connected event         
    def evAtSgactAns(self, evt): 
        if (self.__class__.__log):
            self.logger.debug( function_name()  )
        self._clb(evt)   
 
    #general errors
    def evAtCmeError(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )    
        self.logger.error( function_name() + str(evt))        
        self._clb(evt)  
    
    def evAtHostEEFiles(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )   
        self.logger.error( function_name() + str(evt))        
        self._clb(evt)  
    
    #CSQ - not used..
    def evAtCsq(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )             
        self._clb(evt)
    
    #reconnect procedure, NOT HANDLED yet    
    def evFwSystemReconnect(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )
        self._clb(evt)    
    
    #disconnect events      
    def evFwOffline(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )
        self._clb(evt)
    def evAtNoCarrier(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )  
        self.logger.error( function_name() + str(evt))                
        self._clb(evt)  
    def evFwRecconnetInterval(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )
        self._clb(evt)  
    def evAtSslErrors(self, evt):
        if (self.__class__.__log):
            self.logger.debug( function_name() )
        self.logger.error( function_name() + str(evt))        
        self._clb(evt) 
        

class FwConnStateMachine(StateMachine):
        
    def off_state(self,ev):
        newState = None
        self.logger.debug( function_name()) 
        
        if ev.event =="evFwSwitchOn":            
            newState = "On"
            self.actionGoOnState()
        
        if newState != None:
            self.logger.debug( "new State: " + newState )
        return newState    
    
    def on_state(self, ev):
        newState = None
        #self.logger.debug( function_name()) 
                
        
        if ev.event=="evAtGetIccid":
            self.iccid = ev.str1
        if ev.event == "evAtSgactAns":
            self.ip =  ev.str1
            newState = "Connected"
            self.actionGoToConntected()
        
        if newState != None:
            self.logger.debug( "new State: " + newState )
        return newState
    
    def connected_state(self, ev):
        newState = None
        #self.logger.debug( function_name()) 
                        
        
        if ev.event=="evAtNoCarrier" or ev.event=="evFwOffline" or  ev.event=="evFwRecconnetInterval":
            newState = "disconnected"
            self.actionGoToDisconnected()
        
        #if ev.event=="evFwSwitchOff":
        #    newState = "off"    
        
        if newState != None:
            self.logger.debug( "new State: " + newState )
        return newState

    def disconnected_state(self, ev):
        newState = None
        #self.logger.debug( function_name())               
        
        
        #if ev.event=="evFwSwitchOff":
        #    newState = "off"
        
        if newState != None:
            self.logger.debug( "new State: " + newState )
        return newState


    def stuck_state(self, ev):
        pass
    
    def actionGoToConntected(self):
        self.logger.debug( function_name())
        self.connected_ntimes += 1
        self.logger.info("Connected times " + str(self.connected_ntimes))

        self.connected_session = myTime.getTimestamp()
    
    def actionGoToDisconnected(self):
        self.logger.debug( function_name())
        
        self.disconnected_ntimes += 1
        self.logger.info("Disconnected times " + str(self.disconnected_ntimes))
        
        minutes_session = myTime.getDiffNowMin( self.connected_session  )
        self.connected_total += minutes_session
               
        self.logger.info( "Total minutes Session Connection=" + str(minutes_session) )
        self.logger.info( "Total Overall Connection=" + str(self.connected_total) )
        
        self.logEv("Total minutes Session Connection=" + str(minutes_session))
        self.logEv("Total Overall Connection=" + str(self.connected_total))
    
    def actionGoOnState(self):
        self.logger.debug( function_name())
        self.on_session = myTime.getTimestamp()
    
    #NOT CALLED YET
    def actionGoOffState(self):
        self.logger.debug( function_name())
        self.on_total = myTime.getDiffNowMin( self.on_session  ) 
        
    def printStats(self):
        self.logger.info("Connected times " + str(self.connected_ntimes))
        self.logger.info("Disconnected times " + str(self.connected_ntimes))
        self.logger.info( "Total Overall Connection=" + str(self.connected_total) )
        #print state machine status


    def __init__(self, logEv):
        super(self.__class__, self).__init__()        
        self.evHand = regHandlerConn(self.run)
        self.logEv  = logEv
        
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
        self.iccid=None
        self.ip=None
        
        self.on_session=0
        self.on_total=0
        
        self.connected_ntimes=0
        self.disconnected_ntimes=0

        self.connected_session=0
        self.connected_total=0
              
        self.add_state("Off", self.off_state)
        self.set_start("Off")
        
        self.add_state("On", self.on_state)
        self.add_state("Connected", self.connected_state)
        self.add_state("Disconnected", self.disconnected_state)
        
        #unkown state
        self.add_state("stuck", self.stuck_state)
       
     
     

    