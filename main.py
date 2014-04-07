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

improvements:
- uart has to stop thread when there is an error


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


import datetime
import re

from utils import *
from commands import *

UART_COM = "COM8"
LOG_FOLDER = "logs"
           

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
        
        
class SessionManager:
     def __init__(self):
        self.time = myTime()
        #cerates logfile and logErrorfile            
        self.logFile = LogFile(LOG_FOLDER, self.time)   
        

class sUartM(SessionManager):

    def __init__(self):    
        super(sUartM, self).__init__()                                                    
        self._uart = Uart(UART_COM)            
        self._uart.subscribe(self.time.updTime)                
        self._uart.subscribe(self.logFile.printConsole)
        self._uart.subscribe(self.logFile.writeLog)
       # self.uart.subscribe(Events.parse)                                      
        
        self.fwc= FwCommands(self._uart)                 
       #start the uart thread 
        self._uart.start()        
                
    def closeSession(self):
        self._uart.close_ser()
        self.logFile.closeLog()
        
            

def startLogSession(self):
        #just switch on the device and log all the errors 
        s = sUartM()        
        s.fwc.startFw()
        s.fwc.switchon()
