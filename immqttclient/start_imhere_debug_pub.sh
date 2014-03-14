#!/bin/bash

##########################
#START POSITION PUBLISHER#
##########################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -mn 1 -mi 12345678 -tp devices/log/12345678 -ms "debug message" -sc -sr ssl://localhost:8883