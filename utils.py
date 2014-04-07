'''
Created on 7 Apr 2014

@author: marco
'''

import serial 
import threading
import datetime
import sys,os

class Observable():
    def __init__(self):
        self.lcallback=[]
    
    def subscribe(self, func):
        self.lcallback.append(func)
    
    def fire_action(self, str):
        for func in self.lcallback:
            func(str)


class Uart(threading.Thread, Observable):
    
    def open_ser(self):
        try:
            self.serial_ref = serial.Serial(self.uart_port , baudrate=115200)
        except:
            print "Error on opening port "+ self.uart_port 
            self.serial_ref.close()
     
    def close_ser(self):
        self.serial_ref.close()
        #TODO: stop the THREAD
        
    def __init__(self, port):
        super(Uart,self).__init__(self)
        threading.Thread.__init__(self)        
        self.uart_port=port            
    
    def write(self,str):
        try:
            self.serial_ref.write(str + "\r\n")
        except:
            print "Error on writing on port "+ self.uart_port 
            self.serial_ref.close()    
    
    def readlineCR(self):
        rv = ""    
        while True:
            #if (self.serial_ref.inWaiting() > 0) :
            try:
                ch = self.serial_ref.read()
            except:
                print "Error on reading on port "+ self.uart_port 
                self.serial_ref.close()
                    
            rv += ch
            if ch=='\n':
                return rv
    
    def run(self):
        self.open_ser()
        while True:        
            rcv = self.readlineCR()            
            self.fire_action(rcv)


class LogFile():
    @staticmethod    
    def printConsole(str):
        #print in the shell
        sys.stdout.write(str)
        sys.stdout.flush()
    
    def __init__(self, folder, time):        
        self.time = time      
                
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "/" + folder
        if not os.path.exists(location):
            os.makedirs(location)  
        
        #open lof file
        self.logfile  = open(os.path.join(location, 'log_' + self.time.getLogStr  +'.txt'), 'w')            
        self.logfile.write("\n")
        self.logfile.flush()
        
        #open error file
        self.logErrfile  = open(os.path.join(location, 'logError_' + self.time.getLogStr  +'.txt'), 'w')            
        self.logErrfile.write("\n")
        self.logErrfile.flush()
     
    def writeLog(self,str):
        #append in teh log file                              
        self.logfile.write(self.time() + " " + str + "\n")
        self.logfile.flush()
        
    def writeErrLog(self,str):
        #append in teh log file                              
        self.logErrfile.write(self.time() + " " + str + "\n")
        self.logErrfile.flush()
      
    def closeLog(self):
        #close the log file
        self.logfile.close()
        self.logErrfile.close()


class myFile(Observable):
    
    def __init__(self):
        super(myFile, self).__init__()
                
    def open(self,filename):
        try:
            self.f = open(filename, 'r');
        except IOError:
            print('cannot open file', filename)
    
    def run(self):
        for line in self.f:
            self.fire_action(line)
            
class myTime():        
    def getTime(self):
        return self.datenow
    
    def getLogStr(self):
        return self.datetime.datetime.now().strftime("%H_%M_%S_%f")
    
    def updTime(self, str):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        
    def __init__(self):
        self.datenow = datetime.datetime.now().strftime("%H:%M:%S.%f")   