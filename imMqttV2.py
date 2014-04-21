'''
Created on Apr 21, 2014

@author: marco
'''
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

#SHOULD NOT BE USED
#HAS TO BE INVESTIGATED
logger = logging.getLogger(__name__)        
configureLog(logger)
        
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
 
    def __init__(self, mosServer, callback=None):
        super(self.__class__, self).__init__()
        self._mosServer = mosServer
        self._msgClb=callback
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)

 
    def on_connect(self, mosq, obj, rc):
        #mosq.msubscribe("$SYS/#", 0)
        if MosqAdapter.__log:
            print(self.__class__.__name__ + " Log: on_connect rc: "+str(rc))
    
    def on_message(self, mosq, obj, msg):
        self.log.debug("Received msg " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload) )
        if self._msgClb is not None:            
            self._msgClb(MqtMsgEvent( msg.topic, msg.payload))
        else:
            self.log.error("No handler is defined")
    
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
       
    def subscribe(self, topic, callBack):
        #return code shoudl be kept and used againts the callbck
        #callback should be called when the confirmation is received
        self._mqttc.subscribe(topic)
    
    def unscribe(self, topic):
        self._mqttc.unsubscribe(topic)
        pass
        
    def disconnect(self):
        self._mqttc.disconnect()
  

class MqtDevice():
    def __init__(self, iccid, mosAdapter, mqttEvents):
        self.iccid = iccid
        self.mosAdapter= mosAdapter
        self.mqttEvents = mqttEvents
        
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

        
        self.connected_ntimes=0
        self.connected_session=0
        self.connected_total=0
    
    def _subscribeClb(self):
        #unblock mutex
        #logic should include multiple subsribe and failures..
        #NOT IMPLEMENTED YET
        pass
    
    def subsribe(self):
        topic = "C/" + self.iccid
        ret = self.mosAdapter.subscribe(topic, self.subscribeClb)
        topic = "S/" + self.iccid
        ret = self.mosAdapter.subscribe(topic, self.subscribeClb)
        topic = "D/S/" + self.iccid
        ret = self.mosAdapter.subscribe(topic, self.subscribeClb)
        topic = "D/P/" + self.iccid
        ret = self.mosAdapter.subscribe(topic, self.subscribeClb)
        
    def _online(self):
        self.connected_ntimes += 1
        self.connected_session = myTime.getTimestamp()
        
    def _offline(self):
        #HAS TO BE REPLACED BY AN EV INTERFACE (for grphics)
        #timevents is not logged!
        minutes_session = myTime.getDiffNowMin( self.connected_session  )
        self.connected_total += minutes_session
       
        self.logger.info( "Total minutes Session Connection=" + str(minutes_session) )
        self.logger.info( "Total Overall Connection=" + str(self.connected_total) )
        
        
    def msgClb(self, msg):
        if msg.__class__.__name__ == "MqttMsgHello":
            self._online()
        elif msg.__class__.__name__ == "MqttMsgGoodBye":
            self._offile()
    
    def start(self):
        self._subsribe()
        self.mqttEvents.register(self.iccid, self.msgClb)
        

class MqttEvents(Parseble):
    """
    Implementation of the CallBack Template 
    Real Action has to be implemented here!
    """  
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.registerDev = {}
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)

    def register(self, iccid, clb):
        self.registerDev[iccid] = clb
    
    def unregister(self, iccid):
        del self.registerDev[iccid]
    
    def mqttHello(self, mqtMsgEvent):
        self.log.debug("Hello message")
        self.registerDev[mqtMsgEvent.iccid]()
    
    def mqttGoodbye(self, mqtMsgEvent):
        #action to be difened..!
        self.log.debug("Goodby Will message")
        self.registerDev[mqtMsgEvent.iccid]()
    
    
class Devices():
        def __init__(self, mqttEvents):
            self.devices = {}
            self.mqttEvents = mqttEvents
            self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

        def addDevice(self, iccid, mosAd):
            dev = MqtDevice(iccid, mosAd, self.mqttEvents)
            self.devices[iccid] = dev
        
        def removeDevice(self, index):
            #to implement
            #unsribe from topics
            #unscribe from event handler
            
            pass
        
        def listDevices(self):
            #to implement
            #TODO: a incremental list has to be returned for indexing
            pass
    
class Factory():
    
    def build(self):
        self.ev = MqttEvents()
        self.mAd = MosqAdapter(MqttServer1(), self.ev.callAllFunc)
        
        self.devices = Devices(self.ev)
    
    
    def test1AddDev(self):
        self.devices.addDevice("XXX", self.mAd)
    
    def test1DelDev(self,):
        
        
    
if __name__ == "__main__":
    
        
    