'''
Created on Mar 14, 2014

@author: marco
'''

 import subprocess


clientMqtt="immqttclient/immqttclient.jar"


def send_locatenow():   
    p = subprocess.Popen(["ls", "-l", "/etc/resolv.conf"], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print "Today is", output
    