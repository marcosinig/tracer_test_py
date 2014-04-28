'''
Created on Apr 27, 2014

@author: marco
'''

import logging

from imUtils  import configureLog

logger = logging.getLogger(__name__)        
configureLog(logger)

class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.startState = None
        self.currentState = None
        
        self.handler = None
        
        self._log = logger
        
    def add_state(self, state):
        self.states[state.name.upper()] = state
        state.initState()
        if state.startState:
            self.currentState = state
            self.currentState.acEnterState(None)
    
    def get_State(self, name):
        #get the state in base of the name
        try:
            state = self.states[name.upper()]
        except:
            raise Exception("Not found name=" + name + "in defined states")
        return state
    
    def get_CurrentState(self):
        return self.currentState
        
    def process(self, event):            
        newStateName = self.currentState.processEv(event)
        if newStateName != None:
            self._log.debug( "new State: " + newStateName )
            newState = self.get_State(newStateName)  
            self.currentState.acExitState(event)
            newState.acEnterState(event)
            self.currentState = newState


class StateFath(object):
    def __init__(self, obs):
        self.name = self.__class__.__name__
        self.startState = False
        self._log = logger
        self._obs = obs
    
    def acEnterState(self, event):
        list = self.name.split("_")
        method_name = list[0] + "_enter"
        try:
            method = getattr(self._obs, method_name.lower())
        except:
            return 
        method(event)
    
    def acExitState(self, event):
        list = self.name.split("_")
        method_name = list[0] + "_exit"
        try:
            method = getattr(self._obs, method_name.lower())
        except:
            return 
        method(event)
    
    def initState(self):
        list = self.name.split("_")
        method_name = list[0] + "_init"
        try:
            method = getattr(self._obs, method_name.lower())
        except:
            return 
        method()
    
    def processEv(self, event):
        raise NotImplementedError()
    
    def __str__(self):
        return self.name  

class Test0_state(StateFath):
    
    def __init__(self,obs):
        super(self.__class__, self).__init__(obs)
        self.startState = True        
    
    def acEnterState(self):
        self._log.info("acEnterState " + self.__class__.__name__)
    
    def acExitState(self):
        self._log.info("acExitState"  + self.__class__.__name__)

    def initState(self):
        self._log.info("initState"  + self.__class__.__name__) 
 
    def processEv(self, event):
        self._log.info("processEv"  + self.__class__.__name__)
        if event =="goto2":
            return "Test1_state"
           
        
class Test1_state(StateFath):
    
    def __init__(self, obs):
        super(self.__class__, self).__init__(obs)
    
    #def acEnterState(self):
    #    self._log.info("acEnterState " + self.__class__.__name__)
    
    def acExitState(self):
        self._log.info("acExitState"  + self.__class__.__name__)

 
    def processEv(self, event):
        self._log.info("processEv"  + self.__class__.__name__)   
        

class ObserverTest():
        
    def __init__(self):
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)

    
    def test1_enter(self):
        logger.info("OBS test1_enter ")

    def test2_exit(self):
         logger.info("OBS test2_exit ")    
         
    

if __name__ == "__main__":
    obs = ObserverTest()
    
    sm = StateMachine()
    sm.add_state(Test0_state(obs))
    sm.add_state(Test1_state(obs))
    
    sm.process("goto2")
    str(sm.get_CurrentState())


    
    
    