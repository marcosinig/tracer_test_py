'''
Created on 14/apr/2014

@author: i'm Developer
'''

from imUtils  import *

class Statistics():
    __log=1
    
    def __init__(self):
        self._fwSwitchesOn=0
    
    def _fwSwitchOn(self, str, str2):
        if str2 in function_name():            
            
            if (Statistics.__log==1):
                print "fwSwitchOn"
            
    def _fwReconnect(self, str, str2):
        if str2 in function_name():            
            
            if (Statistics.__log==1):
                print "fwReconnect"
            
    
    def parse(self, str, str2):
        self._fwSwitchOn(str, str2)
        self._fwReconnect(str, str2)