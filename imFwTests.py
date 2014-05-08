'''
Created on May 6, 2014

@author: marco
'''

import imUtils 
import imFwInterface

import time, os, platform, sys

import main          

log = imUtils.logging.getLogger(__name__)        
imUtils.configureLog(log)
         


def testGpsInit(sessMng):
    
    #sessMng.fwCmd.reset()
    #time.sleep(1)
    #TODO: when uart is remount problem with ROOT access
    
    #sessMng.shellCmd.testWaitEv()
    
    #sessMng.shellCmd.fw_simReset()
    sessMng.shellCmd.FwEnableTraces()    
    time.sleep(1)
    if (sessMng.shellCmd.isGsmOn()):
        log.info("GSM on")        
        sessMng.shellCmd.gw_SwitchGps("off")
        sessMng.shellCmd.gw_SwitchGps("on")        
        sessMng.shellCmd.gsmGpioReboot()        
    else:
        sessMng.shellCmd.switchOnGsm()
        log.info("GSM off")
    
    #TODO: test again the gsm status!
        
    sessMng.shellCmd.gsmCmee()
    
    sessMng.shellCmd.gsmAtQss2()
    sessMng.shellCmd.gsmAtQssWait()
    
    sessMng.shellCmd.gsmSetClk()
    
    #sessMng.shellCmd.gsmSgActOn()
    
    for loop in range(100):        
        log.info("LOOP num "+ str(loop) )
        
        
        sessMng.shellCmd.gpsp(1)
        
        
        log.info("CONTEXT ON")       
        
        sessMng.shellCmd.gpsAcp()
        
        #for i in range(10):
        #    sessMng.shellCmd.gpsAcp()
        try: 
            ret = sessMng.shellCmd.gpsM2mLocate()
        except imFwInterface.AtNoConn:            
                sessMng.shellCmd.gsmSgActOn()
                continue           
        except imFwInterface.AtTimeout : 
                continue
        
        if ret == "Ok" :    
            sessMng.shellCmd.gpsInit()           
        sessMng.shellCmd.gpsp(0)
        time.sleep(1)


def startFwTests():
    #just switch on the device and log all the errors 
    global sessMng        
    sessMng = main.UartM()         
    
    sessMng.shellCmd = imFwInterface.ShellCmd(sessMng._uart)
    
    sessMng._events.msubscribe(sessMng.shellCmd.parseEv)       
      
    sessMng.start()
    #try:
    testGpsInit(sessMng)
    
    #except Exception as e:
    #    print e
    #    sessMng.close()
    
    sessMng.close()



if __name__ == '__main__':
    startFwTests()