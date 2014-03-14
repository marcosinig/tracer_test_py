#!/bin/bash

########################
#START STATUS PUBLISHER#
########################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -mn 1 -mi 12345678 -tp devices/status/12345678 -ms "HELLO;hw123;fw123;999;888" -sc -sr ssl://localhost:8883
