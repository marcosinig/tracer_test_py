'''
Created on Mar 14, 2014

@author: marco
'''

import mosquitto
import os
import sys
import threading

#ssl://ec2-54-221-151-14.compute-1.amazonaws.com:8883

class MosqAdapter(threading.Thread): 
 
    ICCID="89372021131217026926"
 
    def on_connect(self, mosq, obj, rc):
        #mosq.subscribe("$SYS/#", 0)
        print("on_connect rc: "+str(rc))
    
    def on_message(self, mosq, obj, msg):
        print("Received msg " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    
    def on_publish(self, mosq, obj, mid):
        print("on_publish mid: "+str(mid))
    
    def on_subscribe(self, mosq, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self, mosq, obj, level, string):
        print("log: "+ string)
    
    def on_disconnect(self, mosq, userdata, rc):
         print("disconnect: " + rc)
    
    def open(self):
        self._mqttc = mosquitto.Mosquitto("MARCO-TEST")
        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe       
        self._mqttc.on_disconnect = self.on_disconnect 
        #self._mqttc.on_log = self.on_log
        
        self._mqttc.username_pw_set("imcloud","hg3686g9FWn102a")
        
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = location +  "\\immqttclient\\client-ca.crt"
        
        if not os.path.exists(location):
            print("CA certificate does not exists " + location)
            sys.exit()
        
         
        self._mqttc.tls_set(location)
        self._mqttc.tls_insecure_set(True)
        self._mqttc.connect("54.204.45.154", 8883, 60)
    
    def run(self):
        self._mqttc.loop_forever()
        
    def subscribe(self):
        ans = self._mqttc.subscribe("C/" + MosqAdapter.ICCID)
        print "Subscribe  ", ans[1:2]
        ans = self._mqttc.subscribe("S/" + MosqAdapter.ICCID)
        print "Subscribe  ", ans[1:2]
        
    def pubHello(self):
        ans = self._mqttc.publish("D/S/" + MosqAdapter.ICCID, "HELLO;1.0;1404031630;0;0;N;N;10.01.000", 2)
        print "Pub Hello  ", ans[1:2]
        
    def pubPosition(self):
        ans = self._mqttc.publish("D/P/" + MosqAdapter.ICCID, "00;FP;140403124052;+45.54491;+11.46344;3;+0;3;3;4100.00;0;222;88;+63;Y", 2)
        print "Pub Position  ", ans[1:2]


        
if __name__ == "__main__":
    m = MosqAdapter()
    m.open()
    m.start()
    m.subscribe()
    m.pubHello()
    m.pubPosition()
   

    
    
    