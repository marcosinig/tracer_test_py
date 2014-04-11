'''
Created on Mar 14, 2014

@author: marco
'''

import mosquitto
import os
import sys
import threading
import time

IP_TLS = "54.204.45.154"
IP_TEST = "54.247.123.48"
ICCID="89372021131217026926"

class MqtMsgEvent():
    def __init__(self, iccid, topic, payload):
        self.iccid = iccid
        self.topic = topic
        self.payload = payload     


class ImMqttMesAction():    
    def hello(self, mqtMsgEvent):
       print ("received HELLO") 
       
    def goodbye(self, mqtMsgEvent):
        print ("received Goodbye") 
    
    def msgClb(self, msg):
        if "HELLO" in msg.payload :
            self.hello(msg)
        if "GOODBYE WILL" in msg.payload:
            self.goodbye(msg)
        
        

class MosqAdapter(threading.Thread): 
 
    def __init__(self, iccid, callback=None):
        super(self.__class__, self).__init__()
        self.iccid = iccid
        self.clb=callback
 
    def on_connect(self, mosq, obj, rc):
        #mosq.subscribe("$SYS/#", 0)
        print("on_connect rc: "+str(rc))
    
    def on_message(self, mosq, obj, msg):
        print("Log: Received msg " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        if self.clb is not None:            
            self.clb.msgClb(MqtMsgEvent(self.iccid, msg.topic, msg.payload))
    
    def on_publish(self, mosq, obj, mid):
        print("Log: on_publish mid: "+str(mid))
    
    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print("Log: Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self, mosq, obj, level, string):
        print("log: "+ string)
    
    def on_disconnect(self, mosq, userdata, rc):
         print("Log: disconnect: ", rc)
    
    def open(self):
        self._mqttc = mosquitto.Mosquitto("MARCO-TEST")
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe       
        self._mqttc.on_disconnect = self.on_disconnect 
        #self._mqttc.on_log = self.on_log
        
        self._mqttc.will_set("D/S/", "GOODBYE WILL", 2)
        
        
        self._mqttc.username_pw_set("imcloud","hg3686g9FWn102a")
        
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "\\immqttclient\\client-ca.crt"
        
        if not os.path.exists(location):
            print("CA certificate does not exists " + location)
            sys.exit()
        
         
        #self._mqttc.tls_set(location)
        #self._mqttc.tls_insecure_set(True)
        self._mqttc.connect(IP_TEST, 8883, 60)
    
    def run(self):
        self._mqttc.loop_forever()
        
    def subscribe(self):
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
    m = MosqAdapter(ICCID)
    m.open()
    m.start()
    m.subscribe()
    m.pubHello()
    m.pubPosition()
   
def testParseHello():
    msgAct = ImMqttMesAction()
    m = MosqAdapter(ICCID, msgAct)
    m.open()
    m.start()
    #TODO: should wait for oprn confirm
    time.sleep(1)    
    m.subscribe()
    #TODO: should wait for sub confirm
    time.sleep(1)
    m.pubHello()
    time.sleep(1)
    m.disconnect()
    time.sleep(1)
    
if __name__ == "__main__":
    testParseHello()
        
    