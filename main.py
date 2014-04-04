'''
Created on Feb 18, 2014

todo:
- implement all At / firmware errors
- implements Events on Uart!
- use packages

- send a command and receive answer in a timeout value
   - the answer has to be evaluated
        -in base of the answe, take some actions
        
-parse info from the command line

Basic Scenario:
1) start logging an trace just the errors..
2) errors has to be counted, have a report of the status (how many connession lost, ...)

3) 


Futuristic:
- gui!

NOT WORKING:
-write log in file.. (changed uart Observable)

@author: I'm
'''
import serial 
import time
import datetime
import re
import threading
import sys,os


UART_COM = "COM8"
LOG_FOLDER = "logs"


class FwCommands():
            
    @staticmethod
    def enable_trace(uart):
        uart.write("trace" + " 2")
    @staticmethod
    def disable_trace(uart):
        uart.write("trace" + " 0")                        
    @staticmethod
    def enable_atflow(uart):
        uart.write("atflow" + " 1")
    @staticmethod
    def disable_atflow(uart):
        uart.write("atflow" + " 0")                         
    @staticmethod
    def switchon(uart):
        uart.write("sim" + " btns")    
    @staticmethod    
    def reset(uart):
        uart.write("sim" + " reset")
    @staticmethod    
    def help(uart):
        uart.write("help")
    @staticmethod
    def gsm(uart,str):
        uart.write("uart"+ " " + str)
        
    @staticmethod    
    def startFw(uart):
        FwCommands().enable_trace(uart)
        FwCommands().enable_atflow(uart)
        FwCommands().switchon(uart)
        
    @staticmethod  
    def onGsm(uart):
        uart.write("gpio 12 0")
        time.sleep(1)
        uart.write("gpio 10 1")
        time.sleep(1)
        uart.write("gpio 10 0")
        time.sleep(1)
 
 
class Observable():
    def __init__(self):
        self.lcallback=[]
    
    def subscribe(self, func):
        self.lcallback.append(func)
    
    def fire_action(self, str):
        for func in self.lcallback:
            func(str)
          

class Events(Observable):            
           
    def cmeError(self, str):
        pat = "(\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(str)
         
    def hostEEFiles(self, str):
        pat = "(\+SIFIXEV: Host EE Files Successfully Created)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(str)
         
    def gpsacp(self, str):
        pat = "(AT\$GPSACP)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(str)
         
    def gpssw(self, str):
        pat = "(AT\$GPSSW)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(str)
    
    def sgact(self, str):
        pat = "(\#SGACT)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(str)
                
            
    def parse(self, str):
        Events().hostEEFiles(str)
        Events().cmeError(str)
        Events().gpsacp(str)
        Events().gpssw(str)
        Events().sgact(str)
        


class LogFile():
    @staticmethod    
    def printConsole(str):
        #print in the shell
        sys.stdout.write(str)
        sys.stdout.flush()
    
    def __init__(self, time):        
        self.time = time      
                
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "/" + LOG_FOLDER
        if not os.path.exists(location):
            os.makedirs(location)  
        
        #open lof file
        self.logfile  = open(os.path.join(location, 'log_' + datetime.datetime.now().strftime("%H_%M_%S_%f")  +'.txt'), 'w')            
        self.logfile.write("\n")
        self.logfile.flush()
        
        #open error file
        self.logErrfile  = open(os.path.join(location, 'logError_' + datetime.datetime.now().strftime("%H_%M_%S_%f")  +'.txt'), 'w')            
        self.logErrfile.write("\n")
        self.logErrfile.flush()
     
    def writeLog(self,str):
        #append in teh log file                              
        self.logfile.write(self.time() + " " + str + "\n")
        self.logfile.flush()
        
    def writeErrLog(self,str):
        #append in teh log file                              
        self.logErrfile.write(self.time() + " " + str + "\n")
        self.logErrfile.flush()
      
    def closeLog(self):
        #close the log file
        self.logfile.close()
        self.logErrfile.close()


class Uart(threading.Thread, Observable):
    
    def open_ser(self):
        try:
            self.serial_ref = serial.Serial(self.uart_port , baudrate=115200)
        except:
            print "Error on opening port "+ self.uart_port 
            self.serial_ref.close()
     
    def close_ser(self):
        self.serial_ref.close()
        #TODO: stop the THREAD
        
    def __init__(self, port=UART_COM):
        Observable.__init__(self)
        threading.Thread.__init__(self)        
        self.uart_port=port            
    
    def write(self,str):
        try:
            self.serial_ref.write(str + "\r\n")
        except:
            print "Error on writing on port "+ self.uart_port 
            #self.serial_ref.close()    
    
    def readlineCR(self):
        rv = ""    
        while True:
            #if (self.serial_ref.inWaiting() > 0) :
            ch = self.serial_ref.read()
            rv += ch
            if ch=='\n':
                return rv
    
    def run(self):
        self.open_ser()
        while True:        
            rcv = self.readlineCR()            
            self.fire_action(rcv)


class SessionManager:
    timeout_loops=60 #seconds
    
    def getTime(self):
        return self.datenow
    
    def updTime(self, str):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        
    def initSession(self):                                
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f") 
        #cerates logfile and logErrorfile            
        self.logFile = LogFile(self.getTime)   
        
        self.uart = Uart()            
        self.uart.subscribe(self.updTime)                
        self.uart.subscribe(self.logFile.printConsole)
        self.uart.subscribe(self.logFile.writeLog)
       # self.uart.subscribe(Events.parse)                                      
                   
       #start the uart thread 
        self.uart.start()
        
                
    def closeSession(self):
        self.uart.close_ser()
        self.logFile.closeLog()
        
            
    def startLogSession(self):
        #just switch on the device and log all the errors        
        FwCommands().startFw(self.uart)
        FwCommands().switchon(self.uart)

       

s = SessionManager()
s.initSession()
