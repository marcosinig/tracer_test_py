'''
Created on Apr 21, 2014

@author: marco
'''

from imUtils import *


class MqtMsgEvent():
    """
    Mqtt Message structure
    """
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload
        self.iccid = self._parseTopic()
        
    
    def _parseTopic(self):
        splitted_txt = self.topic.split("/")
        #the last list member has the topic
        return splitted_txt[len(splitted_txt)]
        
    def __str__(self):
        return "iccid=" + self.iccid + "topic=" + self.topic + "payload=" + self.payload

class MqttMsgHello(MqtMsgEvent):
    """
    'HELLO;1.0;1404141730;0;0;Y;N;10.00.008-B021
    """
    def parse(self):
        list = self.payload.split(';')
        self.hwV = list[1]
        self.fwV = list[2]
        self.commDur = list[3]
        self.maxCommDur = list[4]
        self.still = list[5]
        self.lowBatt = list[6]
        self.telitV = list[7]
        self.event="mqttHello"
    
    def __str__(self):
        return "hwV=" + self.hwV + " fwV=" + self.fwV + "commDur=" + self.commDur + "maxCommDur=" + self.maxCommDur + "still=" +self.still + "lowBatt=" + self.lowBatt + "telitV=" + self.telitV
    
class MqttMsgPosition(MqtMsgEvent):
    """
    00;LN;140414204440;+44.58810;+11.27290;1;-47;2;3;2.20;0;222;10;+33;Y        
    """
    def parse(self):
        list = self.payload.split(';')
        self.msgV = list[0]
        self.msgT = list[1]
        self.timestamp = list[2]
        self.latitude = list[3]
        self.longitude = list[4]
        self.fixStatus = list[5]
        self.altitude = list[6]
        self.charge = list[7]
        self.signal = list[8]
        self.hdop = list[9]
        self.timefix = list[10]
        self.country = list[11]
        self.network = list[12]
        self.temperature = list[13]
        self.online = list[14]
        self.event="mqttPosotion"
        
    def __str__(self):
        #TODO
        pass
    
class MqttMsgSetting(MqtMsgEvent):
    """
    US;140305162623;900;Y;N;N;Y;N;40;N;5;5;0;S/89372021131119023831/0660d2d9-9acd-4d57-b9bc-0bff0e4cd707
    """
    def parse(self):
        list = self.payload.split(';')
        self.timestamp = list[1]
        self.periodFix = list[2]
        self.powerSaving = list[3]
        self.parentalLock = list[4]
        self.sosDenial = list[4]
        self.fallNotification = list[5]
        self.debugLevel = list[6]
        self.ackTopic = list[7]
        self.event="mqttSetting"
    
    def __str__(self):
        #TODO
        pass

class MqttMsgLocateNow(MqtMsgEvent):
     #TODO
    pass

class MqttMsgContinuosTracking(MqtMsgEvent):
     #TODO
    pass

class MqttMsgNewFirmware(MqtMsgEvent):
     #TODO
    pass


class MqttMsgGoodBye(MqtMsgEvent):
    """
    'GOODBYE WILL'      
    """
    def parse(self,str):
        self.event="mqttGoodbye"
        
  
class MqttMsgEvents():
    """
    OBSOLOTE TO REMOVE
    """   
    __log=1
     
    def _hello(self, mqtMsgEvent):
       if self.__class__.__log :
            print(self.__class__.__name__ + " Log: " + function_name())
       mqtMsgEvent.__class__= MqttMsgHello
       mqtMsgEvent.parse()
       
    def _goodbye(self, mqtMsgEvent):
        if self.__class__.__log :
            print(self.__class__.__name__ + " Log: " + function_name()) 
    
    def msgClb(self, msg):
        #entry point per parsare un messaggio
        if "HELLO" in msg.payload :
            self._hello(msg)
        if "GOODBYE WILL" in msg.payload:
            self._goodbye(msg)
            
            
class MqttEvents(Observable, Parseble):
    """
    Called everytime a mqtt message is received
    All functions are called to match the right message.
    """
    
    __log=1
    
    def __init__(self):
        super(self.__class__, self).__init__()
    
    def hello(self, mqtMsgEvent):
        if "HELLO" in mqtMsgEvent.payload :
           if self.__class__.__log :                
               print(self.__class__.__name__ + " Log: " + function_name())
           mqtMsgEvent.__class__= MqttMsgHello
           mqtMsgEvent.parse()
           self.fire_action(mqtMsgEvent)
       
    def goodbye(self, mqtMsgEvent):
        if "GOODBYE WILL" in mqtMsgEvent.payload:
            if self.__class__.__log :
                print(self.__class__.__name__ + " Log: " + function_name())             
            
            

