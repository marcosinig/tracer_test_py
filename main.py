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


from imUtils import *
from imCommands import *

UART_COM = "COM8"
LOG_FOLDER = "logs"         

     
        
class SessionManager(object):
     def __init__(self):
        self.time = myTime()
        #cerates logfile and logErrorfile            
        self.logFile = LogFile(LOG_FOLDER, self.time)   
        

class UartM(SessionManager):

    def __init__(self):    
        super(self.__class__, self).__init__()                                               
        self._uart = Uart(UART_COM)            
        self._uart.subscribe(self.time.updTime)                
        self._uart.subscribe(self.logFile.printConsole)
        self._uart.subscribe(self.logFile.writeLog)
       # self.uart.subscribe(Events.parse)                                      
        
        self.fwc= FwCommands(self._uart)                 
       #start the uart thread 
       
    def start(self):
        self._uart.start()
                
    def close(self):
        self._uart.close_ser()
        self.logFile.closeLog()

class LogFileM(SessionManager):    

    def __init__(self):    
        super(self.__class__, self).__init__()
        self._file = logFile()           
        self._events = Events()
        self._stats  = Statistics()
        
        self._events.subscribe(self._stats.parse)
         
        #self._file.subscribe(self.time.updTime)                
        self._file.subscribe(self.logFile.printConsole)
        self._file.subscribe(self.logFile.writeLog)
        self._file.subscribe(self._events.parse)                                      
                        
    def start(self, fileName):
        self._file.open(fileName)
        self._file.start()
                                
    def closeSession(self):        
        self.logFile.closeLog()                    

def startUartLog():
        #just switch on the device and log all the errors 
        s = UartM()        
        s.fwc.startFw()
        s.fwc.switchon()
        
def startLogFile():
    tera = "C:\\Users\\i'm Developer\\Documents\\teraterm_small.log"
    
    s = LogFileM()
    s.start(tera)
    
if __name__ == "__main__":
    startLogFile()