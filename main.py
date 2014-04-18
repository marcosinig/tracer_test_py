'''
Created on Feb 18, 2014

todo:
- implement all At / firmware errors
- implements ShellEvents on Uart!
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
from imSupervisor import *
from imMqtt import *

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
        self._events = ShellEvents()
                
        self._uart.msubscribe(self.time.updTime)                
        self._uart.msubscribe(self.logFile.printConsole)
        self._uart.msubscribe(self.logFile.writeLog)
        self._uart.msubscribe(self._events.callAllFunc)                                      
        
        self.fwc= FwCommands(self._uart)                 
      
       
    def start(self):
        #start the uart thread
        self._uart.open_ser() 
        self._uart.start()
        
    def close(self):
        self._uart.close_ser()
        self.logFile.closeLog()                

def startUartLog():
    #just switch on the device and log all the errors 
            
    s = UartM()     
    
    s._connProf = ConnectionProfiling()
    
    s._events.msubscribe(s._connProf.evHand.callMatchFuncName)
    
    s.start()
       
    s.fwc.startFw()
    

#*******************

class ParseLogFileM(SessionManager):    

    def __init__(self):    
        super(self.__class__, self).__init__()
        self._file = ReadLogFile()           
        self._events = ShellEvents()
        
         
        #self._file.msubscribe(self.time.updTime)                
        #self._file.msubscribe(self.logFile.printConsole)
        self._file.msubscribe(self.logFile.writeLog)
        
        self._file.msubscribe(self._events.callAllFunc)                                      
                        
    def start(self, fileName):
        self._file.open(fileName)
        self._file.start()
                                
    def closeSession(self):        
        self.ReadLogFile.closeLog()    
        
def startLogFile():
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    ReadLogFile = location + "\\fw_logs\\log_13_03_multiple_send.txt"
    
    prof = ParseLogFileM()
    
    #self._stats  = regHandlerConn()
    prof.connProf = ConnectionProfiling()
                     
    prof._events.msubscribe(prof.connProf.evHand.callMatchFuncName)
    
    prof.start(ReadLogFile)
    

    
if __name__ == "__main__":
    startLogFile()