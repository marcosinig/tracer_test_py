'''
Created on Mar 14, 2014

@author: marco

TODO:
 - implement subscriptions callback


'''

import mosquitto
import os
import sys
import threading
import time
import copy

from imUtils import *


class MqtMsgEvent():
    """
    Mqtt Message structure
    """
    def __init__(self, iccid, topic, payload):
        self.iccid = iccid
        self.topic = topic
        self.payload = payload
    
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
    
    """   
    __log=1
     
    def _hello(self, mqtMsgEvent):
       if self.__class__.__log :
           if self.__class__.__log:
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


class TestMqttEvents(Parseble):
    """
    Implementation of the CallBack Template 
    """  
    def mqttHello(self, mqtMsgEvent):
        #action to be difened..!
        print "TestMqttEvents Hello"
    
    def mqttGoodbye(self, mqtMsgEvent):
        #action to be difened..!
        print "goodbye"


class MqttEvents(Observable, Parseble):
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
                    
    

        
class MqttServer1():
    def __init__(self):
        self.ip="54.204.45.154"
        self.port=8883
        self.tls=1
         
class MqttServerTest():
    def __init__(self):
        self.ip="54.247.123.48"
        self.port=8883
        self.tls=0

class MosqAdapter(threading.Thread, Observable): 
    __log=1
    __debugMqtt=0
    __username="imcloud"
    __password="hg3686g9FWn102a"
 
    def __init__(self, mosServer, iccid, callback=None):
        super(self.__class__, self).__init__()
        self._mosServer = mosServer
        self.iccid = iccid
        self._msgClb=callback
 
    def on_connect(self, mosq, obj, rc):
        #mosq.msubscribe("$SYS/#", 0)
        if MosqAdapter.__log:
            print(self.__class__.__name__ + " Log: on_connect rc: "+str(rc))
    
    def on_message(self, mosq, obj, msg):
        if MosqAdapter.__log:
            print(self.__class__.__name__  + " Log: Received msg " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        if self._msgClb is not None:            
            self._msgClb(MqtMsgEvent(self.iccid, msg.topic, msg.payload))
        #self.fire_action(MqtMsgEvent(self.iccid, msg.topic, msg.payload))
    
    def on_publish(self, mosq, obj, mid):
        if MosqAdapter.__log:
            print(self.__class__.__name__  + " Log: on_publish mid: "+str(mid))
    
    def on_subscribe(self, mosq, obj, mid, granted_qos):
        if MosqAdapter.__log:
            print(self.__class__.__name__  + "Log: Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self, mosq, obj, level, string):        
            print(self.__class__.__name__  + " Log: "+ string)
    
    def on_disconnect(self, mosq, userdata, rc):
        if MosqAdapter.__log:
            print(self.__class__.__name__  + " Log: disconnect: ", rc)
    
    def open(self):
        self._mqttc = mosquitto.Mosquitto("MARCO-TEST")
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe       
        self._mqttc.on_disconnect = self.on_disconnect 
        if MosqAdapter.__debugMqtt :
            self._mqttc.on_log = self.on_log
        
        
        #self._mqttc.will_set("D/S/", "GOODBYE WILL", 2)
            
        self._mqttc.username_pw_set(MosqAdapter.__username,MosqAdapter.__password)
        
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "//immqttclient//client-ca.crt"
        
        if not os.path.exists(location):
            print("CA certificate does not exists " + location)
            sys.exit()
        
        if self._mosServer.tls:
            self._mqttc.tls_set(location)
            self._mqttc.tls_insecure_set(True)
        self._mqttc.connect(self._mosServer.ip, self._mosServer.port, 60)
    
    def run(self):
        self._mqttc.loop_forever()
        
    def msubscribe(self):
        ans = self._mqttc.subscribe("C/" + self.iccid)
        print "Subscribe  ", ans[1:2]
        ans = self._mqttc.subscribe("S/" + self.iccid)
        print "Subscribe  ", ans[1:2]
        ans = self._mqttc.subscribe("D/S/" + self.iccid)
        print "Subscribe  ", ans[1:2]
        ans = self._mqttc.subscribe("D/P/" + self.iccid)
        print "Subscribe  ", ans[1:2]
        
    def pubHello(self):
        ans = self._mqttc.publish("D/S/" + self.iccid, "HELLO;1.0;1404031630;0;0;N;N;10.01.000", 2)
        print "Log: Pub Hello  ", ans[1:2]
        
    def pubPosition(self):
        ans = self._mqttc.publish("D/P/" + self.iccid, "00;FP;140403124052;+45.54491;+11.46344;3;+0;3;3;4100.00;0;222;88;+63;Y", 2)
        print "Log: Pub Position  ", ans[1:2]

    def disconnect(self):
        self._mqttc.disconnect()
  
def testSubscription():
    ICCID="89372021131217026926"
    m = MosqAdapter(MqttServer1(),ICCID)
    m.open()
    m.start()
    m.msubscribe()
    m.pubHello()
    m.pubPosition()
   
def testParseHello():
    ICCID="89372021131217026926"
    msgAct = MqttMsgEvents()
    m = MosqAdapter(MqttServer1(), ICCID, msgAct)
    m.open()
    m.start()
    #TODO: should wait for oprn confirm
    time.sleep(1)    
    m.msubscribe()
    #TODO: should wait for sub confirm
    time.sleep(1)
    m.pubHello()
    time.sleep(1)
    m.disconnect()

def mqttInit(iccid, eventCallbck):
    ev = MqttEvents()
    m = MosqAdapter(MqttServer1(),iccid, ev.callAllFunc)

    ev.msubscribe(eventCallbck.callMatchFuncName)
    
    m.open()
    m.start()
    time.sleep(1)    
    m.msubscribe()
    
       
    
def testEvents():
    ICCID="89372021131217026926"
    
    ev = MqttEvents()
    m = MosqAdapter(MqttServer1(),ICCID, ev.callAllFunc)
    
    callbck = TestMqttEvents()

    ev.msubscribe(callbck.callMatchFuncName)
    
    m.open()
    m.start()
    time.sleep(1)    
    m.msubscribe()
    m.pubHello()
    
if __name__ == "__main__":
    testEvents()
        
    