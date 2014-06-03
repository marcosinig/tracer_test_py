'''
Created on May 6, 2014

@author: marco
'''

import imUtils, imFwInterface, imSystem

import time 

log = imUtils.logging.getLogger(__name__)        
imUtils.configureLog(log)
         


def testGpsInit(sessMng):
    
    #register event handler
    sessMng._events.msubscribe(sessMng.shellCmd.parseEv)       

    #use logger !!!!
    #sessMng.logEv
    pass
    
    #TODO: when uart is remount problem with ROOT access
    #sessMng.shellCmd.fw_simReset()
    #
    pass            
            
    
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


def testHtppDownload(sessMng):
    #drop_conf = False
    drop_conf = False
    
    result_l = []
     #register event handler
    sessMng._events.msubscribe(sessMng.shellCmd.parseEv)       

    if not drop_conf:
        sessMng.shellCmd.setNoPrefix()
        
        sessMng.shellCmd.gsmAtReboot()
    
        sessMng.shellCmd.gsmCmee()
        
        sessMng.shellCmd.gsmAtQss2()
        sessMng.shellCmd.gsmAtQssWait()
        
    sessMng.shellCmd.gsmSgActOff()        
    sessMng.shellCmd.gsmSgActOn()
    
    #sessMng.shellCmd.gsmAyHttpConfig("imhere.imcloud.com")
    sessMng.shellCmd.gsmAyHttpConfig("ephemerides.imcloud.com")
    
    for num in range(1,10):
        try:
            #size = sessMng.shellCmd.gsmAtHttpQuery("/services/imhere/provisioning?iccid=89372021131217048078&firmware=1405082230&fota=10.01.000")
            #size = sessMng.shellCmd.gsmAtHttpQuery("/services/imhere/firmware?version=1405161340&iccid=89372021131217048078")
            
            size = sessMng.shellCmd.gsmAtHttpQuery("/imTracer_1405211205.bin")
            
            if size > 0 :
                #size += 21
                sessMng.shellCmd.gsmAtHttpRcv(size)
        #except imFwInterface.AtEvOk:
        #    result_l.append(str(imFwInterface.AtEvOk))
        except:
            pass 
        num += 1
    
    for res in result_l:
        print res
    
    
def testFastDial(sessMng):
    #drop_conf = False
    drop_conf = False
    
    sessMng._events.msubscribe(sessMng.shellCmd.parseEv)       

    if not drop_conf:
        sessMng.shellCmd.setNoPrefix()
        
        sessMng.shellCmd.gsmAtReboot()
    
        sessMng.shellCmd.gsmCmee()
        
        sessMng.shellCmd.gsmAtQss2()
        sessMng.shellCmd.gsmAtQssWait()
        
    sessMng.shellCmd.gsmSgActOff()        
    sessMng.shellCmd.gsmSgActOn()
    
    
    

def startFwTests():
    #just switch on the device and log all the errors 
    uart_list = { "UART_WIN" : "COM3", "UART_MAC" : "/dev/cu.usbmodemimTrace1", "UART_LINUX" : "/dev/ttyUSB0" }

    global imSystem        
    imSystem = imSystem.FactUartSys(uart_list)         
    
    
      
    imSystem.start()
    
    #testGpsInit(imSystem)
    testHtppDownload(imSystem)
    #except Exception as e:
    #    print e
    #    sessMng.close()
    
    imSystem.close()



if __name__ == '__main__':
    startFwTests()