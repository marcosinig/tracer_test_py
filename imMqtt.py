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
from imMqttInterface import *
from imUtils import *
    

        
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
        
class TestMqttEvents(Parseble):
    """
    Implementation of the CallBack Template 
    Real Action has to be implemented here!
    """  
    def mqttHello(self, mqtMsgEvent):
        #action to be difened..!
        print "TestMqttEvents Hello"
    
    def mqttGoodbye(self, mqtMsgEvent):
        #action to be difened..!
        print "goodbye"
  
def testSubscription():
    ICCID="89372021131217026926"
    m = MosqAdapter(MqttServer1(),ICCID)
    m.open()
    m.start()
    m.msubscribe()
    m.pubHello()
    m.pubPosition()
   
def testParseHello():
    #OBSOLOTE
    
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
        
    