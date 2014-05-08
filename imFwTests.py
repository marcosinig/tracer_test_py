'''
Created on May 6, 2014

@author: marco
'''

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


def testGpsInit(sessMng):
    
    #sessMng.fwCmd.reset()
    #time.sleep(1)
    #TODO: when uart is remount problem with ROOT access
    
    #sessMng.atCmd.testWaitEv()
    
    sessMng.fwCmd.FwEnableTraces()
    time.sleep(1)
    if (sessMng.atCmd.isGsmOn()):
        log.info("GSM on")
        sessMng.fwCmd.switchGps("off")
        sessMng.fwCmd.switchGps("on")        
        sessMng.atCmd.gsmGpioReboot()        
    else:
        sessMng.fwCmd.switchOnGsm()
        log.info("GSM off")
    
    #TODO: test again the gsm status!
        
    sessMng.atCmd.gsmCmee()
    
    sessMng.atCmd.gsmAtQss2()
    sessMng.atCmd.gsmAtQssWait()
    
    sessMng.atCmd.gsmSetClk()
    
    #sessMng.atCmd.gsmSgActOn()
    
    for loop in range(100):        
        log.info("LOOP num "+ str(loop) )
        
        
        sessMng.atCmd.gpsp(1)
        
        
        log.info("CONTEXT ON")       
        
        sessMng.atCmd.gpsAcp()
        
        #for i in range(10):
        #    sessMng.atCmd.gpsAcp()
        try: 
            ret = sessMng.atCmd.gpsM2mLocate()
        except imFwInterface.AtNoConn:            
                sessMng.atCmd.gsmSgActOn()
                continue           
        except imFwInterface.AtTimeout : 
                continue
        
        if ret == "Ok" :    
            sessMng.atCmd.gpsInit()           
        sessMng.atCmd.gpsp(0)
        time.sleep(1)


def startFwTests():
    #just switch on the device and log all the errors 
    global sessMng        
    sessMng = UartM()         
    
    sessMng.fwCmd = imFwInterface.FwCommands(sessMng._uart)
    sessMng.atCmd = imFwInterface.AtCommands(sessMng._uart)
    
    sessMng._events.msubscribe(sessMng.atCmd.parseEv)       
      
    sessMng.start()
    #try:
    testGpsInit(sessMng)
    
    #except Exception as e:
    #    print e
    #    sessMng.close()
    
    sessMng.close()



if __name__ == '__main__':
    startFwTests()