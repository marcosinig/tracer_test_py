'''s
Created on 7 Apr 2014

@author: marco

TODO:
LogFile should open consecutive file name (using now date timestamp)

'''

import serial 
import threading
import datetime
import sys,os
import logging

log = logging.getLogger("imSystem."+ __name__)        



class Observable(object):
    """
    Objects that want to be notified have to register (msubscribe) the entry point function
    The Class that heredits, has to call fire_action and all the subsribers (entry point function) will be called
    """
    def __init__(self):
        self.lcallback=[]
    
    def msubscribe(self, func):
        self.lcallback.append(func)
    
    def fire_action(self, obj):
        #method call when the subscribers want to be notified
        for func in self.lcallback:
            func(obj)

class Parseble(object):
    """
    chiama le funzioni della classe che eredita 
    """
       
    def callAllFunc(self, obj):
        """
        chiama tutte le funzioni della classe che eredita eccetto ...
        """
        for name, method in self.__class__.__dict__.iteritems():
            if callable(method) and name != "__init__" and name != "__module__" and name != "__doc__" and name != "callAllFunc":                                
                if  method(self,obj) == True:
                    break
                                
                #TODO: HAS TO BE OPTIMIZED!!!!!!!!!
                #caller has to retun TRUE and brak it.
    
    def callMatchFuncName(self, obj):
        """
        chiama tutte le funzioni e le confronta il nome dell'event
        """
        for name, method in self.__class__.__dict__.iteritems():
            if name == obj.event:
                method(self,obj)
                break
        
    def defCallBck(self, obj):
        method_name = "defCall"
        #try:
        method = getattr(self.connProf, method_name)
        #except:
             
        method(obj)

def function_name():
    return sys._getframe().f_back.f_code.co_name


class UartLine():
    def __init__(self, timestamp, line):
        self.line = line
        self.timestamp = timestamp
    
    def __str__(self):
        return  self.timestamp + "-" + self.line 
#         
# class Uart2(threading.Thread, Observable):
#                 
#     def __init__(self, port, myTime):                
#         threading.Thread.__init__(self)
#         Observable.__init__(self) 
#         self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)       
#         
#         self._myTime = myTime
#         self._serial_obj=None                
#         self._uart_port=port         
#         self._stop = threading.Event() 
#         
#     def __del__(self):
#         self._log.debug("Called del ")
#         self._stop.set()       
#         if self._serial_obj != None:
#             self._serial_obj.close()
#     
#     def close(self):
#           self._log.debug("Called del ")
#           self._stop.set()       
#           if self._serial_obj != None:
#             self._serial_obj.close()
#     
#     def open_ser(self):
#         try:
#             self._serial_obj = serial.Serial(self._uart_port , baudrate=115200)
#         except:
#             self._log.error("Error on opening port "+ self._uart_port) 
#             self.stop()            
#             raise Exception("Error on opening port "+ self._uart_port);
#      
#     def stop(self):
#         self._log.debug("Called Stop ")
#         self._stop.set()       
#         if self._serial_obj != None:
#             self._serial_obj.close()
#     
#     def write(self,str):        
#         if self._serial_obj == None:
#             raise Exception("Uart not open")         
#         try:            
#             self._serial_obj.write(str + "\r\n")
#         except:
#             self._log.error( "Error on writing on port "+ self._uart_port) 
#             self.stop()
#             raise Exception("Error on writing port "+ self._uart_port);
#     
#     def _readlineCR(self):
#         rv = ""    
#         while True:
#             #if (self._serial_obj.inWaiting() > 0) :
#             try:
#                 ch = self._serial_obj.read()
#             except:
#                 self._log.error("Error on reading on port "+ self._uart_port) 
#                 self._serial_obj.close()
#                 raise Exception("Error on reading port "+ self._uart_port);
#                     
#             rv += ch
#             if ch=='\n':
#                 return rv
#     
#     def run(self):
#         while True:        
#             rcv = self._readlineCR()            
#             self.fire_action(UartLine(myTime.getTime(), rcv))

class Uart(threading.Thread, Observable):
                
    def __init__(self, port):                
        threading.Thread.__init__(self)
        Observable.__init__(self) 
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)       
        
        self._serial_obj=None                
        self._uart_port=port         
        self._stop = threading.Event() 
        

    def close(self):
          self._log.debug("Called del ")
          self._stop.set()       
          if self._serial_obj != None:
            self._serial_obj.close()
    
    def open_ser(self):
        try:
            self._serial_obj = serial.Serial(self._uart_port , baudrate=115200)
        except:
            self._log.error("Error on opening port "+ self._uart_port) 
            self.stop()            
            raise Exception("Error on opening port "+ self._uart_port);
     
    def stop(self):
        self._log.debug("Called Stop ")
        self._stop.set()       
        if self._serial_obj != None:
            self._serial_obj.close()
    
    def write(self,str):        
        if self._serial_obj == None:
            raise Exception("Uart not open")         
        try:            
            self._serial_obj.write(str + "\r\n")
        except:
            self._log.error( "Error on writing on port "+ self._uart_port) 
            self.stop()
            raise Exception("Error on writing port "+ self._uart_port);
    
    def _readlineCR(self):
        rv = ""    
        while True:
            #if (self._serial_obj.inWaiting() > 0) :
            try:
                ch = self._serial_obj.read()
            except:
                self._log.error("Error on reading on port "+ self._uart_port) 
                self._serial_obj.close()
                raise Exception("Error on reading port "+ self._uart_port);
                    
            rv += ch
            if ch=='\n':
                return rv
    
    def run(self):
        while True:        
            rcv = self._readlineCR()            
            self.fire_action(rcv)


class LogFile():
    @staticmethod    
    def printConsole(str):
        #print in the shell
        sys.stdout.write(str)
        sys.stdout.flush()
    
    def __init__(self, folder, time):        
        self._myTime = time   
        self.logfile = None   
        self.logEvent  = None
                
        location =os.path.dirname(os.path.realpath(__file__))  +  "/" + folder
        if not os.path.exists(location):
            os.makedirs(location)  
        
        #open _log file
        self.logfile  = open(os.path.join(location, 'log_' + self._myTime.getLogStr()  +'.txt'), 'w')            
        self.logfile.write("\n")
        self.logfile.flush()
        
        #open Events file
        self.logEvent  = open(os.path.join(location, 'logEvents_' + self._myTime.getLogStr()  +'.txt'), 'w')            
        self.logEvent.write("\n")
        self.logEvent.flush()
        
        print "Writing log uart file in " + self.logfile.name
        print "Writing log Event file in " + self.logEvent.name
        
    def logEv(self, type, str):
        self.LogType[type](str)
     
    def fwLog(self,str):
        #append in teh logEv file                              
        self.logfile.write(self._myTime.getTime() + " " + str + "\n")
        self.logfile.flush()
        
    def evLog(self,str):
        #append in teh logEv file                              
        self.logEvent.write(self._myTime.getTime() + ">> " + str + "\n")
        self.logEvent.flush()
        
        self.fwLog(">> " + str)
                
    def closeLog(self):
        #close the logEv file
        self.logfile.close()
        self.logEvent.close()
        
    #LogType = { FWLOG: _fwLog, "EVLOG" : _evLog }


class ReadLogFile(Observable):
    """
    Class for  reading Fw Log Files
    """
    def __init__(self):
        super(self.__class__, self).__init__()
        self._file = None
                
    def open(self,filename):
        if not os.path.exists(filename):                    
            print "Filename does no exists " + filename
            sys.exit()
        try:
            self._file = open(filename, 'r');
        except IOError:
            print('cannot open file', filename)
    
    def start(self):
        for line in self._file:
            self.fire_action(line)
            
class myTime():     
    
    @staticmethod
    def getTimestamp():
        return datetime.datetime.now()
    @staticmethod
    def getDiffNowMin(dt):
        return (myTime.getTimestamp() - dt).total_seconds() / 60
    
    def getTime(self):
        return self.datenow
    
    def getLogStr(self):
        return datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    
    def updTime(self, str):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        
    def __init__(self):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")   
        

class OldStateMachine(object):
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.handler = None
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)

        
    def add_state(self, name, handler):
        name = name.upper()
        self.handlers[name] = handler
    
    def get_State(self):
        return 
        
    def set_start(self, name):
        self.startState = name.upper()
        self.currentState = self.startState
        try:
            self.handler = self.handlers[self.startState]
        except:
            raise Exception("must call .set_start() before .run()")

    def run(self, cargo):            
        newState = self.handler(cargo)
        if newState != None:
            self._log.debug( "new State: " + newState )
            self.handler = self.handlers[newState.upper()]
            self.currentState = newState   


# def singleton(cls):
#     instances = {}
#     def getinstance():
#         if cls not in instances:
#             instances[cls] = cls()
#         return instances[cls]
#     return getinstance
# @singleton


def configureLog(log):

    #TODO: confguration is wrong,.,
    
    # create _log 
    #logger = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('_log.txt')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher _log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #formatter =  logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the _log
    log.addHandler(fh)
    log.addHandler(ch)
