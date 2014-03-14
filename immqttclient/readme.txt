Requirementes:
- JDK 1.7
- SSL client certificates in dir "cert"

Show options: java -jar immqttclient.jar -h

How to specificy mqtt endpoint:

-TCP: -sr tcp://localhost:1883 -us USERNAME -pa PASSWORD
-SSL: -sc -sr tcp://localhost:1883 -us USERNAME -pa PASSWORD

Usage example (imhere simulator):

1. 	Stress test on MQTT broker with 1000 clients each sending up to 1000 random position messages every 30 seconds 

	java -jar immqttclient.jar -cn 1000 -mt 30 -mn 1000 -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD
	
2.  Send single position to a specif topic

	java -jar immqttclient.jar -cn 1 -mn 1 -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD -qo 1 -mi 12345678 -tp devices/positions/12345678
	
3.  Send log message from device with iccid 12345678

	java -jar immqttclient.jar -mn 1 -mi 12345678 -tp D/L/12345678 -ms "debug message" -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD
	
4.  Send status message HELLO from device with iccid 12345678

	java -jar immqttclient.jar -mn 1 -mi 12345678 -tp D/S/12345678 -ms "HELLO;hw123;fw123;999;888" -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD

    Send status message GOODBYE from device with iccid 12345678 
    
    java -jar immqttclient.jar -mn 1 -mi 12345678 -tp D/S/12345678 -ms "GOODBYE" -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD
    
    Send status message STILL from device with iccid 12345678
    
    java -jar immqttclient.jar -mn 1 -mi 12345678 -tp D/S/12345678 -ms "STILL" -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD
    
5.  Subscribe to commands topic with response OK on ack temporary topic

    java -jar immqttclient.jar -ac -qo 0 -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD -tp C/12345678


Usage example (imcloud simulator):

1. 	Send locate now command to device with iccid 
		
	java -jar immqttclient.jar -cm ln -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD -mn 1 -mi 12345678
	
2. 	Send locate continuous command to device with iccid 
		
	java -jar immqttclient.jar -cm ct -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD -mn 1 -mi 12345678

3. 	Send new firmware command to device with iccid  
		
	java -jar immqttclient.jar -cm nf -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD -mn 1 -mi 12345678

4.  Send settings to device with iccid

	java -jar immqttclient.jar -mn 1 -mi 12345678 -tp S/12345678 -ms "US;<CT>;<TT>;<PS>;<PL>;<SD>;<FN>;<TN>;<HT>;<DN>;<TD>;<TM>;<DB>;<AT>" -sc -sr ssl://localhost:8883 -us USERNAME -pa PASSWORD
