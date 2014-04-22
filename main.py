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
from imFwInterface import *
from imFwConnProfiling import *
import platform


UART_WIN = "COM8"
UART_MAC = "/dev/cu.usbmodemimTrace1"

LOG_FOLDER = "logs"              

#logger = logging.getLogger(__name__)        
#configureLog(logger)

    
class SessionManager(object):
    """
    Common int Session
    """
    
    def __init__(self):
        self.time = myTime()
        #cerates logfile and logErrorfile            
        self.logFile = LogFile(LOG_FOLDER, self.time)  
          
        

class UartM(SessionManager):
    """
    Uart Firmware Manager
    """
    
    def __init__(self):    
        super(self.__class__, self).__init__()                                               
        self._uart = Uart(UartM.returnOsCom())    
        self._events = ShellEvents()
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
                
        self._uart.msubscribe(self.time.updTime)                
        self._uart.msubscribe(self.logFile.printConsole)
        self._uart.msubscribe(self.logFile.fwLog)
        self._uart.msubscribe(self._events.callAllFunc)                                      
        
        self.fwCmd= FwCommands(self._uart)                 
      
    def start(self):
        #start the uart thread
        logger.info("Starting Uart parsing com " + self._uart.uart_port)
        self._uart.open_ser() 
        self._uart.start()
        
    def close(self):
        self._uart.close_ser()
        self.logFile.closeLog()
        
    @staticmethod 
    def returnOsCom():
        if platform.system() == "Windows":
            return UART_WIN
        if platform.system() == "Darwin":
            return UART_MAC               

def startUartLog():
    #just switch on the device and log all the errors 
    global sessMng        
    sessMng = UartM()     
    sessMng._stateMac = FwConnStateMachine(sessMng.logFile.evLog)
    sessMng._events.msubscribe(sessMng._stateMac.evHand.callMatchFuncName)
    
    sessMng.start()
    
    sessMng.fwCmd.FwEnableTraces()
    
    sessMng.simBtns()
    

#*******************

class ParseLogFileM(SessionManager):    

    def __init__(self):    
        super(self.__class__, self).__init__()
        self._file = ReadLogFile()           
        self._events = ShellEvents()
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
        #self._file.msubscribe(self.time.updTime)                
        self._file.msubscribe(self.logFile.printConsole)
        self._file.msubscribe(self.logFile.fwLog)
        self._file.msubscribe(self._events.callAllFunc)                                      
                        
    def start(self, fileName):
        self.logger.info("Starting Parsing");
        self._file.open(fileName)
        self._file.start()
                                
    def closeSession(self):        
        self.ReadLogFile.closeLog()    
        
def startParseLogFile():
    logPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    logPath = logPath + "//fw_logs//log_13_03_multiple_send.txt"
    
    logger.info("Starting ParseLogFile file: " + logPath);
    
    sessMng = ParseLogFileM()
    
    #self._stats  = regHandlerConn()
    sessMng.stMachine = FwConnStateMachine(sessMng.logFile.evLog)
                     
    sessMng._events.msubscribe(sessMng.stMachine.evHand.callMatchFuncName)
    
    sessMng.start(logPath)
    

sessMng = None    
if __name__ == "__main__":
    logger.info("Starting Main");
    #startUartLog()
    #startParseLogFile()
    