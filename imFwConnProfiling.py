'''
Created on 14/apr/2014

@author: i'm Developer

TODO:

-MngListProfEv :
    - l'oggetto non DEVE essere incluso in 

- Rimuovere RegHandlerConn???
    non serve a molto.., forse per i log?!?
    ridondanza nomi..
    DOVREBBE servire per redefinire alcuni eventi con azioni ma far passare tutti gli eventi!

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
    
    """
    __log=1
    
    def __init__(self, clb, logEv):
        super(self.__class__, self).__init__()
        self._clb=clb
        self.logEv= logEv
        self._log = logging.getLogger("imSystem."+ __name__ + "."+ self.__class__.__name__)
    
    def defCallBck(self, evt):
        self._log.debug( str(evt) )
        self._clb(evt)
    
class MngListProfEv():
    
    class ProfEv(object):
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

    class ProfileExEv(ProfEv):
        def __init__(self, connEvents, ev):
            super(self.__class__, self).__init__( connEvents, ev.getSource() +" "+ev.getExceptionType(), ev)
    
    class ProfileStatusEv(ProfEv):
        #not used
        def __init__(self,connEvents, msg, ev, status_p):
            super(self.__class__, self).__init__(connEvents,  ev.getSource() +" "+ev.getExceptionType(), ev, status_p)
    
    class ProfileEvEx(ProfEv):
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
        profEv = MngListProfEv.ProfileExEv(imUtils.myTime.getTimestamp(), ev ) 
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
    

class MngStCnProf():
    class StCnProf():                
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
        self.connEvents = MngListProfEv()
        
        
        self.iccid = None
        self.ip = None
        
        #statistic on device, calculated as the amount of time that is not on the off state
        self.on_session_t = None
        self.on_total_t = 0
        
        #startistics disconnected, updated everytime enter/exit disconnected status
        self.disconnected_nt = -1
        
        self.online_p = MngStCnProf.StCnProf("Online")
        self.disconnected_p = MngStCnProf.StCnProf("Disconnected")
        self.gprs_p = MngStCnProf.StCnProf("Gprs")
        self.provisioning_p = MngStCnProf.StCnProf("Provisioning")
        self.ssl_p = MngStCnProf.StCnProf("Ssl")
        self.mqtt_p = MngStCnProf.StCnProf("Mqtt")
                   
    def __str__(self):
        line1 = ""
        return str(self.connEvents)    
                        
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


class Init_state(imStateMachine.StateFath):
    
    def __init__(self, obs, stateM, shellCmd):
        super(self.__class__, self).__init__(obs)
        self.stateM = stateM
        self.shellCmd = shellCmd
        
        self.startState = True
        self.timer = threading.Timer(5, self.clbNoEvents)                
    
    def clbNoEvents(self):
        self._log.debug("No Events received, go to off state!")
        
        self.shellCmd.fw_TraceOn()
        self.shellCmd.fw_AtFlowOn()
        
        self.stateM.change_state("Off_state", imFwInterface.EventMsg("auto generated event", "auto generated event"))
        self.shellCmd.fw_simBtns()        
    
    def enterState(self, event):
        self._log.debug(function_name())
        
        self._log.info("Started waiting for events..")
        self.timer.start()
        
    def processEv(self, event):
        self._log.debug(function_name())
        
        self._log.info("Event received! Device is not in Off state, Blocked here!")
        self.timer.cancel()
        

class Off_state(imStateMachine.StateFath):
    
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        #self.startState = True
    
    def enterState(self, event):
        self._log.info(function_name())
        
        if self.connProf.on_session_t != None:
            self.on_total_t = imUtils.myTime.getDiffNowMin( self.on_session_t  )        
            #print on_total_t and on_session_t
            pass
            profEv = self.connProf.connEvents.ConnProfileEv(self, "Switching off", event)
            self.connProf.connEvents.addProfEv(profEv)
    
            self.on_session_t = None
              
    def exitState(self, event):
        self._log.info(function_name())         
        self.connProf.on_session_t = imUtils.myTime.getTimestamp()                
        profEv = self.connProf.connEvents.ProfileEvEx(self, "Switched On", event, self.connProf.disconnected_p)
        self.connProf.connEvents.addProfEv(profEv)
        
    def processEv(self, event):
        newState = None

        if event.event == "evFwSysGsmOnFailed":
            self.connProf.connEvents.addProfExEv(event)
        
        if event.event == "evFwSysUserOn":
            newState = "Disconnected_state"
        
        return newState   

class Disconnected_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
    
    def enterState(self, event):
        self._log.info(function_name())   
       
        self.connProf.disconnected_p.enter()
        
        profEv = self.connProf.connEvents.ProfEv(self, "Disconnected Enter", event)
        self.connProf.connEvents.addProfEv(profEv)
        
    def exitState(self, event):
        pass
    
    def processEv(self, event):
        newState = None
        
        if event.event== "evFwSysGpsStartupFailed" or event.event=="evFwSysNvmFailed" or event.event=="evFwSysStartupFailed":  
            self.connProf.connEvents.addProfExEv(event)
        
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
        
    def enterState(self, event):
        self._log.info(function_name())
        
        self.connProf.gprs_p.enter()

        profEv = self.connProf.connEvents.ProfEv(self, "Gprs enter", event) 
        self.connProf.connEvents.addProfEv(profEv)
        
    def exitState(self, event):
        self._log.info(function_name())   
        
        self.connProf.gprs_p.exit()
        #self._log.info(str (self.gprs_p) )
        
        profEv = self.connProf.connEvents.ProfileEvEx( self,"Gprs exit", event, self.connProf.gprs_p) 
        self.connProf.connEvents.addProfEv(profEv)
            
    def processEv(self, event):
        newState = None

        #if event.event == "evAtSgactAns":
        #    self.connProf.set_ip(event.str1)
        
        if event.isExcepton():
            #log the exceptions
            self.connProf.connEvents.addProfExEv(event)
        

        #WARN: Should move on with the evAtSgactAns!
        if event.event == "evAtQueryProvisioning":  
            newState = "Provosioning_state" 
        
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
        
        return newState
    
class Provosioning_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def enterState(self, event):
        self._log.info(function_name())
       
        self.connProf.provisioning_p.enter()

        profEv = self.connProf.connEvents.ProfEv(self, "Provisioning enter", event) 
        self.connProf.connEvents.addProfEv(profEv)
        
    def exitState(self, event):    
        self._log.info(function_name()) 
          
        self.connProf.provisioning_p.exit()
        self._log.info(str (self.connProf.provisioning_p) )
        
        profEv = self.connProf.connEvents.ProfileEvEx(self, "Provisioning exit", event, self.connProf.provisioning_p) 
        self.connProf.connEvents.addProfEv(profEv)
        
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self.connProf.connEvents.addProfExEv(event)       
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evAtRingOk":
            newState = "Ssl_state"   
            #WARN: should move on with the answer
        
        return newState

class Ssl_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def enterState(self, event):
        self._log.info(function_name())
       
        self.connProf.ssl_p.enter()

        profEv = self.connProf.connEvents.ProfEv(self,"Ssl enter", event) 
        self.connProf.connEvents.addProfEv(profEv)
        
    def exitState(self, event):  
        self._log.info(function_name())   
          
        self.connProf.ssl_p.exit()
        self._log.info(str (self.connProf.ssl_p) )
        
        profEv = self.connProf.connEvents.ProfileEvEx( self,"Ssl exit", event, self.connProf.ssl_p) 
        self.connProf.connEvents.addProfEv(profEv)
            
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self.connProf.connEvents.addProfExEv(event)
        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state" 
                    
        if event.event == "evFwMqttConnect":
            newState = "MqttConn_state"   
        
        return newState

class MqttConn_state(imStateMachine.StateFath):

    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
    
    def enterState(self, event):
        self._log.info(function_name())
        
        self.connProf.mqtt_p.enter()

        profEv = self.connProf.connEvents.ProfEv(self, "Mqtt enter", event) 
        self.connProf.connEvents.addProfEv(profEv)
        
    def exitState(self, event):
        self._log.info(function_name())  
         
        self.connProf.mqtt_p.exit()
        self.connProf._log.info(str (self.connProf.mqtt_p) )
        
        profEv = self.connProf.connEvents.ProfileEvEx( self,"Mqtt exit", event, self.connProf.mqtt_p) 
        self.connProf.connEvents.addProfEv(profEv) 
    
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self.connProf.connEvents.addProfExEv(event)

        
        if event.event=="evFwRecconnetInterval":
            newState = "Disconnected_state"        
                    
        if event.event == "evFwSystemOnLine":
            newState = "Online_state"   
            #self.connProf.go_gprs_on(event)
        
        return newState

class Online_state(imStateMachine.StateFath):
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
        
    def enterState(self, event):    
        self._log.info(function_name())   
        
        self.connProf.disconnected_p.exit()
        profEv = self.connProf.connEvents.ProfileEvEx(self, "Disconnected Exit", event, self.connProf.disconnected_p)
        self.connProf.connEvents.addProfEv(profEv) 
        
        self.connProf.online_p.enter()
        
        profEv = self.connProf.connEvents.ProfEv(self, "Online Enter", event)
        self.connProf.connEvents.addProfEv(profEv)
    
    def exitState(self, event):
        self._log.info(function_name())   
        
        self.connProf.online_p.exit()
        #self._log.info(str (self.online_p) )
        #copy_p = copy.deepcopy(self.online_p)
        
        profEv = self.connProf.connEvents.ProfileEvEx(self, "Online Exit", event, self.connProf.online_p)
        self.connProf.connEvents.addProfEv(profEv) 
            
    def processEv(self, event):
        newState = None

        if event.isExcepton():
            #log the exceptions
            self.connProf.connEvents.addProfExEv(event)
                    
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
                            

def startDevStateProf(imSys):
    """
    This is a singleton, TODO: it has to be implemnted according
    """                            
    imSys.stateM = imStateMachine.StateMachine()
    
    evHand = RegHandlerConn(imSys.stateM.process, imSys.logFile.logEv)        
    connProf = MngStCnProf(imSys.logFile.logEv)        
   
    #NOT USED YET: self.shellCmd = shellCmd        
    #TODO IMPLEMENT A WAY TO DO A RESET
    
        
    imSys._events.msubscribe(evHand.defCallBck)
    #imSys._events.msubscribe(evHand.callMatchFuncName)

    imSys.stateM.add_state(Init_state(connProf, imSys.stateM, imSys.shellCmd))
    
    imSys.stateM.add_state(AtStuck_state(connProf))
    imSys.stateM.add_state(FwStuck_state(connProf))
    
    imSys.stateM.add_state(Off_state(connProf))
    imSys.stateM.add_state(Disconnected_state(connProf))
    imSys.stateM.add_state(Gprs_state(connProf))
    imSys.stateM.add_state(Provosioning_state(connProf))
    imSys.stateM.add_state(Ssl_state(connProf))
    imSys.stateM.add_state(MqttConn_state(connProf))
    imSys.stateM.add_state(Online_state(connProf))
    
    
def printReport(connProf):
        print("\n Start Report \n")
        print str(connProf())
           
      
