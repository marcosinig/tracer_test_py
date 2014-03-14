#!/bin/bash

##########################
#START POSITION PUBLISHER#
##########################

JAVA_HOME=/home/ubuntu/jdk

cd `dirname $0`

$JAVA_HOME/bin/java -jar immqttclient.jar -mi 12345678 -mn 1 -tp settings/12345678 -ms "US;<CT>;<TT>;<PS>;<PL>;<SD>;<FN>;<TN>;<HT>;<DN>;<TD>;<TM>;<DB>;<AT>" -sc -sr ssl://localhost:8883