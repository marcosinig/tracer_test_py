'''
Created on Feb 18, 2014

todo:

-implement uart line obj
-implement profiling events

- implements ShellEvents on Uart!
- use packages

- send a command and receive answer in a timeout value
   - the answer has to be evaluated
        -in base of the answe, take some actions
        
-parse info from the command line

improvements:


Basic Scenario:



Futuristic:
- gui!

NOT WORKING:


@author: I'm
'''

import datetime


from imUtils import *
from imFwInterface import *
from imFwConnProfiling import *
import platform
import time


UART_WIN = "COM8"
UART_MAC = "/dev/cu.usbmodemimTrace1"

LOG_FOLDER = "logs"              

#_log = logging.getLogger(__name__)        
#configureLog(_log)

    
class SessionManager(object):
    """
    Common int Session
    """
    
    def __init__(self):
        self._myTime = myTime()
        #cerates logfile and logErrorfile            
        self.logFile = LogFile(LOG_FOLDER, self._myTime)  
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
    
          
        

class UartM(SessionManager):
    """
    Uart Firmware Manager
    """
    
    def __init__(self):    
        super(self.__class__, self).__init__()   
        self._log.info("Called init ")
                                                    
        self._uart = Uart(UartM.returnOsCom())    
        self._events = ShellEvents()       
                
        self._uart.msubscribe(self._myTime.updTime)                
        self._uart.msubscribe(self.logFile.printConsole)
        self._uart.msubscribe(self.logFile.fwLog)
        self._uart.msubscribe(self._events.callAllFunc)                                      
        
        self.fwCmd= FwCommands(self._uart)     
        
    def __del__(self):
        self._log.info("Called del ")
        del self._uart
        del self._events
          
      
    def start(self):
        #start the uart thread
        logger.info("Starting Uart parsing com " + self._uart._uart_port)
        self._uart.open_ser() 
        self._uart.start()
        
    def close(self):
        self._uart.close()
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
    
    sessMng.fwCmd.simBtns()
    
    #_myTime.sleep(1)
    
    #del sessMng
    
    
    

#*******************

class ParseLogFileM(SessionManager):    

    def __init__(self):    
        super(self.__class__, self).__init__()
        self._file = ReadLogFile()           
        self._events = ShellEvents()
        self._log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
        #self._file.msubscribe(self._myTime.updTime)                
        self._file.msubscribe(self.logFile.printConsole)
        self._file.msubscribe(self.logFile.fwLog)
        self._file.msubscribe(self._events.callAllFunc)                                      
                        
    def start(self, fileName):
        self._log.info("Starting Parsing");
        self._file.open(fileName)
        self._file.start()
                                
    def closeSession(self):        
        self.ReadLogFile.closeLog()    
        
def startParseLogFile():                
    logPath =  os.getcwd()  + "//fw_logs//log_13_03_multiple_send.txt"
    logger.info("Starting ParseLogFile file: " + logPath);

    
    global sessMng    
    sessMng = ParseLogFileM()
    
    #self._stats  = regHandlerConn()
    sessMng.stMachine = FwConnStateMachine(sessMng.logFile.evLog)
                     
    sessMng._events.msubscribe(sessMng.stMachine.evHand.callMatchFuncName)
    
    sessMng.start(logPath)
    

sessMng = None    
if __name__ == "__main__":
    logger.info("Starting Main");
    startUartLog()
    #startParseLogFile()
    