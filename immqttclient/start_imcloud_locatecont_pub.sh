#!/bin/bash

##########################
#START POSITION PUBLISHER#
##########################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -cm ct -sc -sr ssl://localhost:8883 -mn 1 -mi 12345678