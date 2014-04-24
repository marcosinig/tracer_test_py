#!/bin/bash

############################
#START POSITION PUBLICATION#
############################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -cn 1 -mn 1 -sc -sr ssl://localhost:8883 -qo 1 -tp devices/positions/12345678