'''
Created on Feb 18, 2014

todo:

-file path in base of OS
- ospatch not working in windows!!!!
-DO NOT USE IMPORT ALL
       

improvements:






Futuristic:
- gui!

NOT WORKING:
-write log in file.. (changed uart Observable)

@author: I'm
'''

#import datetime


import imUtils 
import imFwInterface
import imFwConnProfiling 

import time, os, platform, sys


UART_WIN = "COM8"
UART_MAC = "/dev/cu.usbmodemimTrace1"
UART_LINUX = "/dev/ttyACM0"

LOG_FOLDER = "logs"              

log = imUtils.logging.getLogger(__name__)        
imUtils.configureLog(log)

    
class SessionManager(object):
    """
    Common int Session
    """
    
    def __init__(self):
        self.time = imUtils.myTime()
        #cerates logfile and logErrorfile            
        self.logFile = imUtils.LogFile(LOG_FOLDER, self.time)  
          
        

class UartM(SessionManager):
    """
    Uart Firmware Manager
    """
    
    def __init__(self):    
        super(self.__class__, self).__init__()                                               
        self._uart = imUtils.Uart(UartM.returnOsCom())    
        self._events = imFwInterface.ShellEvents()
        self._log = imUtils.logging.getLogger(__name__ + "." + self.__class__.__name__)
                
        self._uart.msubscribe(self.time.updTime)                
        self._uart.msubscribe(self.logFile.printConsole)
        self._uart.msubscribe(self.logFile.fwLog)
        self._uart.msubscribe(self._events.callAllFunc)                                      
        
                           
    def start(self):
        #start the uart thread
        self._uart.open_ser()
        self._log.info("Starting Uart parsing com " + self._uart._uart_port) 
        self._uart.start()
        
    def close(self):
        self._uart.close()
        self.logFile.closeLog()
        
    @staticmethod 
    def returnOsCom():
        if platform.system() == "Windows":
            return UART_WIN
        elif platform.system() == "Darwin":
            return UART_MAC   
        elif platform.system() == "Linux":
            return UART_LINUX  

def startUartLog():
    #just switch on the device and log all the errors 
    global sessMng        
    sessMng = UartM() 
    sessMng.shellCmd = imFwInterface.ShellCmd(sessMng._uart)
        
    sessMng.stMachine = imFwConnProfiling.FactryStateMachine(sessMng.logFile.evLog, sessMng.shellCmd)
    sessMng._events.msubscribe(sessMng.stMachine.evHand.callMatchFuncName)
    
    
    sessMng.start()
    
    #sessMng.fwCmd.FwEnableTraces()
    
    #sessMng.fwCmd.simBtns()
    
    #sessMng.stMachine.printReport()
    
    
    

#*******************

class ParseLogFileM(SessionManager):    

    def __init__(self):    
        super(self.__class__, self).__init__()
        self._file = imUtils.ReadLogFile()           
        self._events = imFwInterface.ShellEvents()
        self._log = imUtils.logging.getLogger(__name__ + "." + self.__class__.__name__)
        
        #self._file.msubscribe(self.time.updTime)                
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
    #logPath =  os.path.dirname(os.path.realpath(__file__))  
    logPath = os.getcwd()
    #logPath = logPath + "\\fw_logs\\log_13_03_multiple_send.txt"
    logPath = os.path.join (logPath + 'fw_logs' + 'log_13_03_multiple_send.txt')
    #logPath = "C:\\Users\\i'm Developer\\Documents\\log_imhere\\connction_problem\\log_sos_2_23_04.txt"
    log.info("Starting ParseLogFile file: " + logPath);

    
    global sessMng    
    sessMng = ParseLogFileM()
    
    #sessMng.connProf = ConnProfiling(sessMng.logFile.evLog)
    sessMng.stMachine = imFwConnProfiling.FactryStateMachine( sessMng.logFile.evLog)
                     
    sessMng._events.msubscribe(sessMng.stMachine.evHand.callMatchFuncName)
    
    sessMng.start(logPath)
    
    sessMng.stMachine.printReport()
    
    

sessMng = None    
if __name__ == "__main__":
    log.info("Starting Main");
    startUartLog()
    #startParseLogFile()
    