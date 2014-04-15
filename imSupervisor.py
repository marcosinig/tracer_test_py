'''
Created on 14/apr/2014

@author: i'm Developer
'''

from imUtils  import *
from imCommands import *


class Statistics(Parseble):
    __log=1
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self._fwSwitchesOn=0
    
    def fwSwitchOn(self, evt):
        if (Statistics.__log):
            print "fwSwitchOn"
            
    def fwReconnect(self, evt):
        if (Statistics.__log):
            print "fwReconnect"

    def _iccid(self, evt):            
        if (Statistics.__log):
            print "_iccid " + evt.str1            
