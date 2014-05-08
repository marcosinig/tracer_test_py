'''
Created on 7 Apr 2014

@author: marco
'''

import time,datetime
import re
import sys
import threading 

from  imUtils import function_name
import imUtils

logger = imUtils.logging.getLogger("imSystem."+ __name__)        

    
class AtError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class AtNoConn(AtError):
    def __init__(self, value):
        AtError.__init__(self, value)
class AtTimeout(AtError):
    def __init__(self, value):
        AtError.__init__(self, value)
class AtEvNotExpect(AtError):
    def __init__(self, value):
        AtError.__init__(self, value)

class ShellCmd():
    
    def __init__(self, uart):
        self.__uart=uart
        self._log = imUtils.logging.getLogger("imSystem."+ __name__ + "."+ self.__class__.__name__)
        
        self.listEvExp = None
        self.eventWait = threading.Event()     
        self.timer = None
        self.evRecv = None
        self.waitTimError = None
    
    def parseEv(self, evRecv):
        self._log.debug("Parsing ev " + str(evRecv)) 
        if (self.listEvExp != None):
            for ev in self.listEvExp:
                self.evRecv = evRecv  
                if evRecv.event ==  ev:                      
                    self.releaseWait() 
                elif evRecv.event == "evAtError":                    
                    self.raisErrEv("Received " + evRecv.event + " instead of ")                    
                #else:                
                #    self.raiseError("Received " + evRecv.event + " instead of ")
    
        
    def raisErrTimeout(self, strEr):
        #function called when timeout is expired        
        #self.cleanWaitEv()               
        #raise AtTimeout(strEr + str(self.listEvExp))
        self.waitTimError = strEr
        self.eventWait.set()
    
    def raisErrEv(self, strEr):
        #self.cleanWaitEv()   
        self.timer.cancel()     
        raise AtEvNotExpect(strEr + str(self.listEvExp))
   
    def releaseWait(self):
        #called when the event is received
        self.timer.cancel()                 
        self._log.debug("Mutex will be released")
        self.eventWait.set()              
    
    def waitEv(self, listEvExp, timeout):
        self.listEvExp = listEvExp
        self.waitTimError = None
        self.timer = threading.Timer(timeout, self.raisErrTimeout, ["Timeout waiting "])
        self._log.debug("wait for timeout" + str (timeout))        
        self.timer.start()
        self.eventWait.clear()
        self.eventWait.wait()
        self._log.debug("get Out from wait" + str (timeout))
        
        self.timer.join()
        if self.waitTimError != None :
            raise AtTimeout(self.waitTimError + str(self.listEvExp))


    def testWaitEv(self):                
        
        self.setWaitEv(["NullEv"])        
        self.waitEv(6.0)
        return 
    
    ############
    #TODO: the stuff above should be moved outside 
    ############# 
        
    def switchOnGsm(self):                
        self.__uart.write("gpio 12 1")
        time.sleep(1)
        self.__uart.write("gpio 12 0")        
        self.waitEv(["evAtHostEEFiles"], 6.0)
        return  
        
        
    def gsmCmee(self): 
        self._log.debug("gpsp")
        
        self.__uart.write("gsm  AT+CMEE=2")                   
        self.waitEv(["evAtOk"], 2.0)
        return

    def gsmAtReboot(self):
        self.__uart.write("gsm  at#reboot")        
        self.waitEv(["evAtOk"], 2.0)
        self.waitEv(["evAtHostEEFiles"], 6.0)        
  
        return  
    
    def gsmGpioReboot(self):            
        self.__uart.write("gpio 15 1")
        time.sleep(1)
        self.__uart.write("gpio 15 0")
        self.waitEv(["evAtHostEEFiles"], 6.0)        
        self.waitEv(["evAtGpsPatched"], 6.0)
        return  
    
    def isGsmOn(self):
        self._log.debug("isGsmOn")
        
        self.__uart.write("gpio 2")        
        self.waitEv(["evFwGpio"], 1.0)        
        if (self.evRecv.str1 == '1'):
            return True
        else: 
            return False

    def gsmAtQss2(self): 
        self._log.debug("gpsp")
        
        self.__uart.write("gsm  AT#QSS=2")               
        self.waitEv(["evAtOk"], 2.0)
        return

    def gsmAtQssWait(self): 
        self._log.debug("gsmAtQssWait")
        
        self.__uart.write("gsm  AT#QSS?")               
        self.waitEv(["evAtQss"], 2.0)
        while True:   
            if self.evRecv.str1 != "3" :
                time.sleep(1)
            else:            
                break                        
        return
   
                
    def gpsp(self, state): 
        self._log.debug("gpsp")
        
        self.__uart.write("gsm AT$GPSP=" + str(state))               
        self.waitEv(["evAtOk"], 2.0)
        return
    
    def gsmSgActOn(self): 
        self._log.debug("gpsp")        
        
        while( True ):
            self.__uart.write("gsm AT#SGACT=1,1,"",""")                   
            self.waitEv(["evAtSgactAns", "evAtCmeError"], 4.0)
            if self.evRecv.event == "evAtCmeError" and "context already activated" in self.evRecv.str1 :
                break
            if self.evRecv.event == "evAtCmeError" :
                time.sleep(1)
            elif self.evRecv.event == "evAtSgactAns":
                break
        return    
    
    def gsmSetClk(self):
        self._log.debug("gsmClk")                    
        self.__uart.write("gsm AT+CCLK=\"" + datetime.datetime.now().strftime("%y/%m/%d,%H:%M:%S+00")  + "\"" )               
        self.waitEv(["evAtOk"], 3.0)    
        return
            

    def gpsAcp(self): 
        self._log.debug("gpsAcp")
        
        self.__uart.write("gsm AT$GPSACP")               
        self.waitEv(["evAtGpsacp"], 2.0)
        if self.evRecv.str1 == "" :
            #TODO HOW TO MANAGE IT ???
            #should start from the beginning
            self._log.debug("ERROR gpsAcp")
        return     
    
    def gpsM2mLocate(self):
        self._log.debug("gpsM2mLocate")
        
        self.__uart.write("gsm AT#AGPSSND")               
        self.waitEv(["evAtAgpsRing", "evAtCmeError"], 100.0)
        
        if self.evRecv.event== "evAtCmeError" and (" Can not resolve name" in self.evRecv.line  or " operation not supported" in self.evRecv.line ):
            raise AtNoConn("Not connected")
        
        list = self.evRecv.str1.split(",")
        if list[0] == "200" :
            return "Ok"
        
        return 
            
    def gpsInit(self):
        self._log.debug("gpsInit ")                
        self.__uart.write("gsm AT$GPSINIT")       
        self.setWaitEv(["evAtOk"])        
        self.waitEv(1.0)        
        return     
    
    ################################################
    
    def fw_TraceOn(self):
        self.__uart.write("trace" + " 2")
    
    def fw_TraceOff(self):
        self.__uart.write("trace" + " 0")                        
    
    def fw_AtFlowOn(self):
        self.__uart.write("atflow" + " 1")
    
    def fw_AtFlow_off(self):
        self.__uart.write("atflow" + " 0")                         
            
    def fw_simReset(self):
        self.__uart.write("sim reset")        
    
    def fw_Gsm(self):
        self.__uart.write("gsm")
        
    def FwEnableTraces(self):
        self.fw_TraceOn()
        self.fw_AtFlowOn()
    
    def fw_simBtns(self):
        self.__uart.write("sim" + " btns")    
    
    def gw_SwitchGps(self, status):
        if status == "on" :
            self.__uart.write("gpio 10 0")
        elif status == "off":
            self.__uart.write("gpio 10 1")
     


#####################################################
        
class EventMsg():
    def __init__(self, line, event, str1=""):
        #uart line that has generate the event
        self.line=line
        #event name
        self.event=event
        #optional parameter
        self.str1 = str1
    
    def isErrorEvent(self):
        if self.event[-5:] == "Error":
            return True
        return False
    
    def isFaultEvent(self):
        if self.event[-6:] == "Failed":
            return True
        return False
    
    def isExcepton(self):
        if self.isFaultEvent() or self.isErrorEvent():
            return True
        return False
    
    def getExceptionType(self):
        #return xxxxxXXXXXX
        #evAtCmeError -> At
        if  self.isFaultEvent():
                return "Failed"
        if  self.isErrorEvent():
                return "Error"
        
    def getSource(self):
        #return xxXXxxx
        #evAtCmeError -> At
        return  self.event[2:4]
    
    def isAtEvent(self):
        if self.getSource() == "At" :
            return True
        return False
    
    def isFwEvent(self):
        if self.getSource() == "Fw" :
            return True
        return False
        
    def __str__(self):        
        return "Event= " + self.event + " line= " + self.line + " str = " +self.str1 
     

class AutoEvents():
    """ 
    Events generates by state machine
    """
    def evFwAutoStuck(self, str):
        return (EventMsg(str, function_name()))
    def evAtAutoStuck(self, str):
        return (EventMsg(str, function_name()))
        


class ShellEvents(imUtils.Observable, imUtils.Parseble):
    
    def __init__(self):
        super(self.__class__, self).__init__()

    def evFwGpio(self, str):
        if "gpio" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 6 :
                self.fire_action(EventMsg(str, function_name(), splitted_txt[5]))      
                return True
        return False   
    
    def evAtOk(self, str):
        if "OK" in str:
            self.fire_action(EventMsg(str, function_name()))      
            return True
        return False 
                    
    def evAtCmeError(self, str):
        pat = "(\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name(), matchObj.group(2)))      
            return True
        return False
    
    #TODO: It has to be parsed with CME since it matches with CME ERROR
    def evAtError(self, str):
        pat = "ERROR"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name()))      
            return True
        return False
    
    def evAtQss(self, str):
        if "#QSS:" in str:
            splitted_txt = str.split( )
            self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))      
            return True
        return False   
    
    def evAtAgpsRing(self, str):
        if "#AGPSRING:" in str:
            splitted_txt = str.split( )
            self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))      
            return True
        return False           
       
    def evFwSysGpsStartupFailed(self, str):
        if "GPS configuration failed" in str:
            self.fire_action(EventMsg(str, function_name()))        
            return True
        return False
    
    def evFwSysGsmOnFailed(self, str):
        if "GSM status set ON failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False        
    def evFwSysGsmOFffFailed(self, str):
        if "GSM status set OFF failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False         
    def evAtHostEEFiles(self, str):
        if "SIFIXEV: Host EE Files Successfully Created" in str:
            self.fire_action(EventMsg(str, function_name()))                                             
            return True
        return False            
    def evFwSysStartupFailed(self, str):
        if "System startup failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False            
    def evFwSysNvmFailed(self, str):
        if "System NVM configuration failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False                            
    def evAtGpsacp(self, str):                        
        pat = "(\$GPSACP:)(.*)"                
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            self.fire_action(EventMsg(str, function_name(), matchObj.group(2)))
            return True
        return False    
    def evAtSgactQuery(self, str):
        if "AT#SGACT" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False    
    def evAtSgactAns(self, str):
        if "#SGACT" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                #check it is an IP address
                ip_addr = splitted_txt[1].split('.')
                if len(ip_addr) == 4:
                    self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
                    return True
        return False                    
    def evFwGprsActFailed(self, str):
        if "System gprs connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evAtQueryProvisioning(self, str):
         if "AT#HTTPQRY=" in str and "provisioning" in str:
            self.fire_action(EventMsg(str, function_name()))   
            return True
         return False
        
    def evFwProvisioningFailed(self, str):
        if "System provisioning failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evAtRingOk(self, str):
        if "#HTTPRING: 0,200,\"text/plain;charset=UTF-8\"" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False    
        
    def evAtSsls(self, str):
        if "AT#SSLS=1" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evAtSsld(self, str):
        if "AT#SSLD" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwSystemTlsFailed(self, str):
        if "System tls connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
       
    def evFwMqttConnect(self, str):
        if "MQTT connect" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttConnectFailed(self, str):
        if "System mqtt connection failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttSusbscribedFailed(self, str):
        if "System mqtt subscribe failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evFwMqttHelloFailed(self, str):
        if "System mqtt hello failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttPubFailed(self, str):
        if "MQTT publish locations failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwMqttPingFailed(self, str):
        if "MQTT ping failed" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False           
    
    def evFwSystemOnLine(self, str):
        if "System online" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
                
    def evAtCsq(self, str):
        if "+CSQ" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name()))     
                return True
        return False
            
    def evAtNoCarrier(self, str):
        if "NO CARRIER" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False

    def evFwButtonOnOff(self, str):
        if "BUTTON_MANAGER_EVENT_ONOFF received" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False            

                                
    def evFwSysUserOn(self, str):
        if "SYS user on" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    def evFwSysUseOff(self, str):
        if "SYS user off" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
        
    def evFwOffline(self, str):
        if "System NOT online" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False
    
    
    def evAtGetIccid(self, str):
        if "#CCID" in str:
            splitted_txt = str.split( )
            if len(splitted_txt) == 2:
                self.fire_action(EventMsg(str, function_name(), splitted_txt[1]))
                return True
        return False
       
                 
    def evFwRecconnetInterval(self, str):
        if "Reconnect interval waiting" in str:
            splitted_txt = str.split( )
            timeout = splitted_txt[2]            
            self.fire_action(EventMsg(str, function_name(), timeout))
            return True
        return False
                       
    def evAtGpsPatched(self, str):
        if "Patch Manager: Patched" in str:
            self.fire_action(EventMsg(str, function_name()))
            return True
        return False 
                

def test_print(ev):
    print "Found " + str(ev) 


def test_ShellEvents():
    def test_print(ev):
        print "Found " + str(ev)
        
    sh = ShellEvents()
    sh.msubscribe(test_print)
    
    str = "AT#HTTPQRY=#0,0,\"/services/imhere/provisioning?iccid=89372021131119023740&firmware=140306093111"    
    #str = "Reconnect interval waiting"
    #str = " +CME ERROR: sss"
    #str = "#CCID  1 "
    str = "AT#SSLD=1,8883,54.204.45.147,1,1"
    str = "gpio  2 I        GSM_POWERGOOD B01 1"
    str = "+CME ERROR: context already activated"
    #str = "ERROR"
    str = "#QSS: 2,1"
    #str = "#QSS: 3"

    sh.callAllFunc(str)

def test_IsSourceEvent():
    def test_(ev):
        print "Found " #+ str(ev)
        if (ev.isFwEvent()):
            print "Is Fw ev "
        if (ev.isAtEvent()):
            print "Is At ev "
        
    sh = ShellEvents()
    sh.msubscribe(test_)
    
    str = "AT#SSLD="
    #str = "Reconnect interval waiting"
    sh.callAllFunc(str)

if __name__ == "__main__":
    #test_ShellEvents()
    test_IsSourceEvent()
        
            
 
