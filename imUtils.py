'''s
Created on 7 Apr 2014

@author: marco
'''

import serial 
import threading
import datetime
import sys,os

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
                method(self,obj)
    
    def callMatchFuncName(self, obj):
        """
        chiama tutte le funzioni e le confronta il nome dell'event
        """
        for name, method in self.__class__.__dict__.iteritems():
            if name == obj.event:
                method(self,obj)
               

def function_name():
    return sys._getframe().f_back.f_code.co_name

class Uart(threading.Thread, Observable):
                
    def __init__(self, port):
        #super(self.__class__, self).__init__()
        
        threading.Thread.__init__(self)
        Observable.__init__(self)        
        
        self.serial_ref=None
        
        #threading.Thread.__init__(self)        
        self.uart_port=port  
    
    def open_ser(self):
        try:
            self.serial_ref = serial.Serial(self.uart_port , baudrate=115200)
        except:
            print "Error on opening port "+ self.uart_port 
            self.stop()            
            raise Exception("Error on opening port "+ self.uart_port);
     
    def close_ser(self):
        self.serial_ref.close()
        #TODO: stop the THREAD           
    
    def write(self,str):
        
        if self.serial_ref == None:
            raise Exception("Uart not open") 
        
        try:            
            self.serial_ref.write(str + "\r\n")
        except:
            print "Error on writing on port "+ self.uart_port 
            #self.serial_ref.close()   
            #self.stop()
            raise Exception("Error on writing port "+ self.uart_port);
    
    def readlineCR(self):
        rv = ""    
        while True:
            #if (self.serial_ref.inWaiting() > 0) :
            try:
                ch = self.serial_ref.read()
            except:
                print "Error on reading on port "+ self.uart_port 
                self.serial_ref.close()
                    
            rv += ch
            if ch=='\n':
                return rv
    
    def run(self):
         #self.open_ser()
        while True:        
            rcv = self.readlineCR()            
            self.fire_action(rcv)


class LogFile():
    @staticmethod    
    def printConsole(str):
        #print in the shell
        sys.stdout.write(str)
        sys.stdout.flush()
    
    def __init__(self, folder, time):        
        self.time = time      
                
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "/" + folder
        if not os.path.exists(location):
            os.makedirs(location)  
        
        #open lof file
        self.logfile  = open(os.path.join(location, 'log_' + self.time.getLogStr()  +'.txt'), 'w')            
        self.logfile.write("\n")
        self.logfile.flush()
        
        #open error file
        self.logErrfile  = open(os.path.join(location, 'logError_' + self.time.getLogStr()  +'.txt'), 'w')            
        self.logErrfile.write("\n")
        self.logErrfile.flush()
     
    def writeLog(self,str):
        #append in teh log file                              
        self.logfile.write(self.time.getTime() + " " + str + "\n")
        self.logfile.flush()
        
    def writeErrLog(self,str):
        #append in teh log file                              
        self.logErrfile.write(self.time.getTime() + " " + str + "\n")
        self.logErrfile.flush()
      
    def closeLog(self):
        #close the log file
        self.logfile.close()
        self.logErrfile.close()


class ReadLogFile(Observable):
    
    def __init__(self):
        super(self.__class__, self).__init__()
                
    def open(self,filename):
        if not os.path.exists(filename):                    
            print "Filename does no exists " + filename
            sys.exit()
        try:
            self.f = open(filename, 'r');
        except IOError:
            print('cannot open file', filename)
    
    def start(self):
        for line in self.f:
            self.fire_action(line)
            
class myTime():     
    
    def getTime(self):
        return self.datenow
    
    def getLogStr(self):
        return datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    
    def updTime(self, str):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        
    def __init__(self):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")   
        

class StateMachine(object):
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.handler = None
        

    def add_state(self, name, handler):
        name = name.upper()
        self.handlers[name] = handler
        

    def set_start(self, name):
        self.startState = name.upper()
        try:
            self.handler = self.handlers[self.startState]
        except:
            raise Exception("must call .set_start() before .run()")

    def run(self, cargo):            
        newState = self.handler(cargo)
        if newState != None:
            self.handler = self.handlers[newState.upper()]  