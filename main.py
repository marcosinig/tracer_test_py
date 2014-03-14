'''
Created on Feb 18, 2014

@author: I'm
'''
import serial 
import time
import datetime
import re
import threading
import sys,os


class FwCommands():
            
    @staticmethod
    def enable_trace(uart):
        uart.write("trace" + " 1")
    @staticmethod
    def disable_trace(uart):
        uart.write("trace" + " 0")                        
    @staticmethod
    def enable_atflow(uart):
        uart.write("atflow" + " 1")
    @staticmethod
    def disable_atflow(uart):
        uart.write("atflow" + " 0")                         
    @staticmethod
    def switchon(uart):
        uart.write("sim" + " btns")    
    @staticmethod    
    def reset(uart):
        uart.write("sim" + " reset")
    @staticmethod    
    def help(uart):
        uart.write("help")
    @staticmethod
    def gsm(uart,str):
        uart.write("uart"+ " " + str)
    
    @staticmethod    
    def startFw(uart):
        FwCommands().enable_trace(uart)
        FwCommands().enable_atflow(uart)
        FwCommands().switchon(uart)
        
    @staticmethod  
    def onGsm(uart):
        uart.write("gpio 12 0")
        time.sleep(1)
        uart.write("gpio 10 1")
        time.sleep(1)
        uart.write("gpio 10 0")
        time.sleep(1)
 
          

class Events():
    @staticmethod       
    def cmeError(str):
        pat = "(\+CME ERROR:) (.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            print "FOUND " +str
    @staticmethod     
    def hostEEFiles(str):
        pat = "(\+SIFIXEV: Host EE Files Successfully Created)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            print "FOUND!!!!!!!! " +str
    @staticmethod     
    def gpsacp(str):
        pat = "(AT\$GPSACP)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            print "FOUND!!!!!!!! " +str
    @staticmethod     
    def gpssw(str):
        pat = "(AT\$GPSSW)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            print "FOUND!!!!!!!! " +str
    @staticmethod
    def sgact(str):
        pat = "(\#SGACT)(.*)"
        matchObj = (re.match( pat, str, re.M)) 
        if matchObj: 
            print "FOUND!!!!!!!! " +str
                
    @staticmethod        
    def parse(str):
        Events().hostEEFiles(str)
        Events().cmeError(str)
        Events().gpsacp(str)
        Events().gpssw(str)
        Events().sgact(str)
        


class LogFile():
    @staticmethod    
    def printConsole(str):
        sys.stdout.write(str)
        sys.stdout.flush()
    
    def __init__(self, time):
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  
        self.time = time      
        self.logfile  = open(os.path.join(location, 'log.log'), 'w')            
        self.logfile.write("\n")
        self.logfile.flush()
     
    def writeLog(self,str):                              
        self.logfile.write(self.time() + " " + str + "\n")
        self.logfile.flush()
      
    def closeLog(self):
        self.logfile.close()


class Uart(threading.Thread):
    
    def open_ser(self):
        try:
            self.serial_ref = serial.Serial("/dev/"+ self.uart_port , baudrate=115200)
        except:
            print "Error on opening port "+ self.uart_port 
            self.serial_ref.close()
     
    def close_ser(self):
        self.serial_ref.close()
        
    def __init__(self, lcallback=[], session="ses1", port="ttyACM0"):
        threading.Thread.__init__(self)        
        self.uart_port=port
        self.session=session
        self.lcallback=lcallback
       
    
    def process(self,str):
        for func in self.lcallback:
            func(str)
    
    def write(self,str):
        try:
            self.serial_ref.write(str + "\r\n")
        except:
            print "Error on writing on port "+ self.uart_port 
            #self.serial_ref.close()    
    
    def readlineCR(self):
        rv = ""    
        while True:
            #if (self.serial_ref.inWaiting() > 0) :
            ch = self.serial_ref.read()
            rv += ch
            if ch=='\n':
                return rv
    
    def run(self):
        self.open_ser()
        while True:        
            rcv = self.readlineCR()            
            self.process(rcv)


class SessionManager:
    timeout_loops=60 #seconds
    
    def getTime(self):
        return self.datenow
    
    def updTime(self, str):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        
    def initSession(self, num_loops=3):
        self.start_session=datetime.datetime.now()
        self.num_loops=num_loops
                
        
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f") 
                    
        self.logFile = LogFile(self.getTime)   
        
        self.callbacks=[]
        self.callbacks.append(self.updTime)                
        self.callbacks.append(self.logFile.printConsole)
        self.callbacks.append(self.logFile.writeLog)
        self.callbacks.append(Events.parse)              
                        
        self.uart = Uart(self.callbacks)        
        
        self.atc = AtCommands(self.uart)
        self.uart.start()
        
        
    
    def startSession(self):        
        FwCommands().startFw(self.uart)
        #TODO init timeout per end loop

       

s = SessionManager()
s.initSession()
