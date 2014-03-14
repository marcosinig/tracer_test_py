#!/bin/bash

########################
#START STATUS PUBLISHER#
########################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -mn 1 -mi 12345678 -tp devices/status/12345678 -ms "STILL" -sc -sr ssl://localhost:8883
