'''
Created on 8 May 2014

@author: marco
'''
import imUtils, imFwInterface 

import platform


LOG_FOLDER = "logs"              

log = imUtils.logging.getLogger("imSystem."+ __name__)        


    
class SessionManager(object):
    """
    Common int Session
    """
    
    def __init__(self):
        self.time = imUtils.myTime()
        #cerates logfile and logErrorfile            
        self.logFile = imUtils.LogFile(LOG_FOLDER, self.time)          
        #HAS TO BE VERIFIED!
        #self.log = imUtils.logging.getLogger(__name__)        
        #imUtils.configureLog(self.log)
        

class FactUartSys(SessionManager):
    """
    Uart Firmware Manager
    """
    
    def __init__(self, uart_com):    
        super(self.__class__, self).__init__()                                               
        self._uart = imUtils.Uart(self.returnOsCom(uart_com))    
        self._events = imFwInterface.ShellEvents()
        self._log = imUtils.logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.shellCmd = imFwInterface.ShellCmd(self._uart, self._events)
                
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
        
 
    def returnOsCom(self, uart_com):
        if platform.system() == "Windows":
            return uart_com["UART_WIN"]
        elif platform.system() == "Darwin":
            return uart_com["UART_MAC"]   
        elif platform.system() == "Linux":
            return uart_com["UART_LINUX"]  
        
                

class FactParseLogSys(SessionManager):    

    def __init__(self, logPath):    
        super(self.__class__, self).__init__()
        self._file = imUtils.ReadLogFile()           
        self._events = imFwInterface.ShellEvents()
        self._log = imUtils.logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._logPath = logPath
        
        #self._file.msubscribe(self.time.updTime)                
        self._file.msubscribe(self.logFile.printConsole)
        self._file.msubscribe(self.logFile.fwLog)
        self._file.msubscribe(self._events.callAllFunc)                                      
                        
    def start(self):
        self._log.info("Starting Parsing");
        self._file.open(self._logPath)
        self._file.start()
                                
    def close(self):        
        self.ReadLogFile.closeLog()  