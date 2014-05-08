'''
Created on 14/apr/2014

@author: i'm Developer

TODO:

- implementare il print report fatto BENE:
    - uno breve
    - uno esteso

- Modo per scatenare  il print report da shell durante log??
    - scrivere log in una window??

- implementare reset al BOOT
- Check_Tracer_Status 

Verificare:

Improvements:
 
'''
import imUtils  
import imFwInterface 
import imStateMachine
import logging
import copy,threading
from  imUtils import function_name

logger = imUtils.logging.getLogger("imSystem."+ __name__)        


class RegHandlerConn(imUtils.Parseble):
    """
    function names are called in base of shell and mqtt events
    
    """
    __log=1
    
    def __init__(self, clb, stateMachine, logEv):
        super(self.__class__, self).__init__()
        self._clb=clb
        self.stateM = stateMachine
        self.logEv= logEv
        self._log = logging.getLogger("imSystem."+ __name__ + "."+ self.__class__.__name__)
        
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
        

         

class MngProfEv():
    
    class ConnProfileEv(object):
        def __init__(self, connEvents, msg, ev, status_p = None, errors_ev_list = None):
            #obj has to implement to string
            self.timestamp = imUtils.myTime.getTimestamp()
            self.connEvents = connEvents
            self.msg = msg
            self.ev = ev
            self.status_p = None
            #status report
            if status_p != None:
                self.status_p = copy.deepcopy(status_p)
            #list of all the possible errors
            self.error_ev_list = errors_ev_list
        
        def __str__(self):
            #TODO write in base of what is present in nice way
            line = str( "\n" + self.timestamp.strftime("%H:%M:%S")  ) + " - " + self.msg + " - " #+ str(self.ev)
            if self.status_p != None:
                line += "- \n\t" + str(self.status_p)
            if self.error_ev_list != None:
                line += "- \n\t"
                for errL in self.error_ev_list:
                    line += str( errL )        
            return line 

    class ConnProfExEv(ConnProfileEv):
        def __init__(self, connEvents, ev):
            super(self.__class__, self).__init__( connEvents, ev.getSource() +" "+ev.getExceptionType(), ev)
    
    class ConnProfStatusEv(ConnProfileEv):
        #not used
        def __init__(self,connEvents, msg, ev, status_p):
            super(self.__class__, self).__init__(connEvents,  ev.getSource() +" "+ev.getExceptionType(), ev, status_p)
    
    class ConnProfileEvEx(ConnProfileEv):
        def __init__(self, connEvents, msg, ev, status_p):
            super(self.__class__, self).__init__( connEvents, ev.getSource() , ev, status_p)

    
    def __init__(self):
        #list of all the events reported by the profile class
        self.eventsProf = []
        #list of all the errors, it has to be empty everytime a state is exited
        self.eventsException = []
    
    def addProfExEv(self, ev):
        #self._log.info(function_name())
        #self._log.info(ev.getSource() +": Error in state " + state + "ev: " + ev)
        profEv = MngProfEv.ConnProfExEv(imUtils.myTime.getTimestamp(), ev ) 
        self.eventsException.append(ev)  
    
    def addProfEv(self, ev):
        self.eventsProf.append(ev)  
        #self._log.info(ev)
        
    def __str__(self):
        text=""
        for e in self.eventsProf:
            text += str(e)
        return text
        
        pass
    def getProfEv(self):
        #not used yet
        return copy.deepcopy(self.eventsProf)
        pass
      
    def getAllExEv(self):
        #removes all the event, should change name???
        temp = copy.deepcopy(self.eventsException)
        del self.eventsException
        self.eventsException = []
        return temp  
    

class ConnProfiling():
    class State_Profiling():                
        def __init__(self, stateName):
            self.data = { 'state_Name': stateName,'numTimes':0, 'total_time':0, 'session_ts':None, 'session_min':0 }            
        
        def enter(self):               
            self.data['session_ts'] = imUtils.myTime.getTimestamp()
            self.data['numTimes'] += 1 
            return  self.data['numTimes']
        
        def exit(self):
            if self.data['session_ts'] != None:
                self.data['session_min'] = imUtils.myTime.getDiffNowMin( self.data['session_ts']  )
                self.data['total_time'] +=  self.data['session_min']
                self.data['session_ts'] = None
        
        def __str__(self):
            line1 = "State {state_Name} last session duration min {session_min} overall durations min {total_time} activated ntimes {numTimes}"
            return line1.format(**self.data)
            
    def __init__(self, logEv):
        self._log = logging.getLogger("imSystem."+ __name__ + "."+ self.__class__.__name__)
        self.logEv = logEv
        self.connEvents = MngProfEv()
        
        
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
               
    
    def __str__(self):
        line1 = ""
        return str(self.connEvents)
    
    def off_enter(self, ev): 
       pass
    
                                    
    def off_exit(self, ev):
        pass
    
    
    def disconnected_enter(self, ev):  
        self._log.info(function_name())   
       
        self.disconnected_p.enter()
        
        profEv = self.connEvents.ConnProfileEv(self, "Disconnected Enter", ev)
        self.connEvents.addProfEv(profEv)
                    
    def disconnected_exit(self, ev):        
        pass                                                                 
        
    
    def online_enter(self, ev):
        self._log.info(function_name())   
        
        self.disconnected_p.exit()
        profEv = self.connEvents.ConnProfileEvEx(self, "Disconnected Exit", ev, self.disconnected_p)
        self.connEvents.addProfEv(profEv) 
        
        self.online_p.enter()
        
        profEv = self.connEvents.ConnProfileEv(self, "Online Enter", ev)
        self.connEvents.addProfEv(profEv)
    
    def online_exit(self, ev):
        self._log.info(function_name())   
        
        self.online_p.exit()
        #self._log.info(str (self.online_p) )
        #copy_p = copy.deepcopy(self.online_p)
        
        profEv = self.connEvents.ConnProfileEvEx(self, "Online Exit", ev, self.online_p)
        self.connEvents.addProfEv(profEv) 
   
    def gprs_enter(self, ev):
        self._log.info(function_name())
        
        self.gprs_p.enter()

        profEv = self.connEvents.ConnProfileEv(self, "Gprs enter", ev) 
        self.connEvents.addProfEv(profEv)
    
    def gprs_exit(self, ev):
        self._log.info(function_name())   
        
        self.gprs_p.exit()
        #self._log.info(str (self.gprs_p) )
        
        profEv = self.connEvents.ConnProfileEvEx( self,"Gprs exit", ev, self.gprs_p) 
        self.connEvents.addProfEv(profEv)
         
    def provisioning_enter(self, ev):
        self._log.info(function_name())
       
        self.provisioning_p.enter()

        profEv = self.connEvents.ConnProfileEv(self, "Provisioning enter", ev) 
        self.connEvents.addProfEv(profEv)
    
    def provisioning_exit(self, ev):
        self._log.info(function_name()) 
          
        self.provisioning_p.exit()
        self._log.info(str (self.provisioning_p) )
        
        profEv = self.connEvents.ConnProfileEvEx(self, "Provisioning exit", ev, self.provisioning_p) 
        self.connEvents.addProfEv(profEv)
            
    def ssl_enter(self, ev):
        self._log.info(function_name())
       
        self.ssl_p.enter()

        profEv = self.connEvents.ConnProfileEv(self,"Ssl enter", ev) 
        self.connEvents.addProfEv(profEv)
    
    def ssl_exit(self, ev):
        self._log.info(function_name())   
          
        self.ssl_p.exit()
        self._log.info(str (self.ssl_p) )
        
        profEv = self.connEvents.ConnProfileEvEx( self,"Ssl exit", ev, self.ssl_p) 
        self.connEvents.addProfEv(profEv)
    
    def mqttConn_enter(self, ev):
        self._log.info(function_name())
        
        self.mqtt_p.enter()

        profEv = self.connEvents.ConnProfileEv(self, "Mqtt enter", ev) 
        self.connEvents.addProfEv(profEv)
    
    def mqttConn_exit(self, ev):
        self._log.info(function_name())  
         
        self.mqtt_p.exit()
        self._log.info(str (self.mqtt_p) )
        
        profEv = self.connEvents.ConnProfileEvEx( self,"Mqtt exit", ev, self.mqtt_p) 
        self.connEvents.addProfEv(profEv)             
                        
    def set_iccid(self, iccid):
        self.iccid=iccid
    def set_ip(self, ip):
        self.ip = ip


class AtStuck_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)

class FwStuck_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
                


class Off_state(imStateMachine.StateFath):
    
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        self.startState(True)
    
    def acEnterState(self, event):
        self._log.info(function_name())
        
        if self._obs.on_session_t != None:
            self.on_total_t = imUtils.myTime.getDiffNowMin( self.on_session_t  )        
            #print on_total_t and on_session_t
            pass
            profEv = self._obs.connEvents.ConnProfileEv(self, "Switching off", event)
            self.connEvents.addProfEv(profEv)
    
            self.on_session_t = None
              
    def acExitState(self, event):
        self._log.info(function_name())         
        self._obs.on_session_t = imUtils.myTime.getTimestamp()                
        profEv = self._obs.connEvents.ConnProfileEvEx(self, "Switched On", event, self._obs.disconnected_p)
        self.connEvents.addProfEv(profEv)
        
    def processEv(self, event):
        newState = None

        if event.event == "evFwSysGsmOnFailed":
            self._obs.connEvents.addProfExEv(event)
        
        if event.event == "evFwSysUserOn":
            newState = "Disconnected_state"
        
        return newState   

class Disconnected_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def processEv(self, event):
        newState = None
        
        if event.event== "evFwSysGpsStartupFailed" or event.event=="evFwSysNvmFailed" or event.event=="evFwSysStartupFailed":  
            self._obs.connEvents.addProfExEv(event)
        
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

class Gprs_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        #if event.event == "evAtSgactAns":
        #    self.connProf.set_ip(event.str1)
        
        if event.isExcepton():
            #log the exceptions
            self._obs.connEvents.addProfExEv(event)
        

        #WARN: Should move on with the evAtSgactAns!
        if event.event == "evAtQueryProvisioning":  
            newState = "Provosioning_state" 
        
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
        
        return newState
    
class Provosioning_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self._obs.connEvents.addProfExEv(event)       
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evAtRingOk":
            newState = "Ssl_state"   
            #WARN: should move on with the answer
        
        return newState

class Ssl_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self._obs.connEvents.addProfExEv(event)
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evFwMqttConnect":
            newState = "MqttConn_state"   
        
        return newState



class MqttConn_state(imStateMachine.StateFath):

    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self._obs.connEvents.addProfExEv(event)

        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state"        
                    
        if event.event == "evFwSystemOnLine":
            newState = "Online_state"   
            #self.connProf.go_gprs_on(event)
        
        return newState

class Online_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
            
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self._obs.connEvents.addProfExEv(event)
                    
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state"
        
        if event.event=="evFwSysUseOff":
            newState = "off_state"
            self.init_off()            
            
        return newState

class Check_Tracer_Status():
    """
    this class has to check:
    - fw is stuck: no activity for the last x seconds: it is stuck
       - check has to be executed only when it is not switched_off state
    - gsm interface is stuck: only trace commands and not at activity!
    
    TODO: 
     get state reference
     force to go in a state 
    
    """
    #num consecutive fw events for going in at stuck
    fw_command_threshold = 15
    timeout_fw_stuck = 15.0
    
    def __init__(self, stateMachine):
        self.fw_commands = 0
        self.sm = stateMachine

        self.timer = threading.Timer(Check_Tracer_Status.timeout_fw_stuck, self.no_activity_handler)        
    
    def no_activity_handler(self):
        #function to be schedule after xsec timeout
        print "firmware seems to be stcuk"
        #TODO: string = !!!!

        self.sm.change_state("FwStuck_state", imFwInterface.AutoEvents.evFwAutoStuck(str ))
        
    def process(self, event):
        if event.isAtEvent() :
            self.fw_commands = 0
        if event.isFwEvent() :
            self.fw_commands +=1
        if self.fw_commands > Check_Tracer_Status.fw_command_threshold:
            print "at command interface seems to be stcuk!!"
            #TODO: str = !!!!
            self.sm.change_state("AtStuck_state", imFwInterface.AutoEvents.evAtAutoStuck( str))
        
        if str(self.sm.get_CurrentState) != "...." :
            #here should be reset the timeout..
            self.timer.start() #check how can be reset to INITAL value
                            

def startDevStateProf(sessMng):
    """
    This is a singleton, TODO: it has to be implemnted according
    """
                    
        
    stateM = imStateMachine.StateMachine()
    
    evHand = RegHandlerConn(stateM.process, sessMng.logEv)        
    connProf = ConnProfiling(sessMng.logEv)        
   
    #NOT USED YET: self.shellCmd = shellCmd        
    #TODO IMPLEMENT A WAY TO DO A RESET
    
        
    sessMng._events.msubscribe(evHand.callMatchFuncName)

    
    stateM.add_state(AtStuck_state(connProf))
    stateM.add_state(FwStuck_state(connProf))
    
    stateM.add_state(Off_state(connProf))
    stateM.add_state(Disconnected_state(connProf))
    stateM.add_state(Gprs_state(connProf))
    stateM.add_state(Provosioning_state(connProf))
    stateM.add_state(Ssl_state(connProf))
    stateM.add_state(MqttConn_state(connProf))
    stateM.add_state(Online_state(connProf))
    
    return connProf
    
def printReport(connProf):
        print("\n Start Report \n")
        print str(connProf())
           
      
