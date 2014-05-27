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

import imSystem, imUtils, imFwConnProfiling
import os, logging

uart_list = { "UART_WIN" : "COM3", "UART_MAC" : "/dev/cu.usbmodemimTrace1", "UART_LINUX" : "/dev/ttyACM0" }

def startUartLog():
    #just switch on the device and log all the errors 
    global imSys        
    imSys = imSystem.FactUartSys(uart_list) 
    
    log.info("Starting ParseLogFile file: " + imSys._uart.getName());
        
    imFwConnProfiling.startDevStateProf(imSys)    
    
    imSys.start()
    
    #imSys.close()
   
    #sessMng.stMachine.printDevStateProf()
            
#*******************

  
        
def startParseLogFile():                
    #logPath =  os.path.dirname(os.path.realpath(__file__))  
    #logPath = logPath + "\\fw_logs\\log_13_03_multiple_send.txt"
    #logPath = "C:\\Users\\i'm Developer\\Documents\\log_imhere\\connction_problem\\log_sos_2_23_04.txt"
    
    logPath = os.getcwd()    
    logPath = os.path.join (logPath, 'fw_logs',  'log_13_03_multiple_send.txt')
    
    
    log.info("Starting ParseLogFile file: " + logPath);
    
    global imSys    
    imSys = imSystem.FactParseLogSys(logPath)
    
    #sessMng.connProf = ConnProfiling(sessMng.logFile.evLog)
    imFwConnProfiling.startDevStateProf(imSys)
                                 
    imSys.start()
    
    #str(imSys.connProf)
    
    

sessMng = None    
if __name__ == "__main__":
    
    log = logging.getLogger("imSystem")        
    imUtils.configureLog(log)
    
    log.info("Starting Main");
    startUartLog()
    #startParseLogFile()
    