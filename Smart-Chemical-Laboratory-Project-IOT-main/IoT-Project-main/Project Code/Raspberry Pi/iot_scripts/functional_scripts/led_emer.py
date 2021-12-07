#!/usr/bin/python3.7
import RPi.GPIO as GPIO
import time
#import json
import paho.mqtt.client as mqtt

#mqtt
topic = "iot/actuators/emerlight"
topic2 = "iot/pddl/emerlight"
host = "192.168.178.20"

# time interval
interval = 5

# compare bool
oldval = 1

# set gpio mode to board
GPIO.setmode(GPIO.BOARD)

# set gpio pin 37 to output and low
GPIO.setup(33, GPIO.OUT)
GPIO.output(33, GPIO.LOW)

try:
    def on_message(client, userdata, message):
        #print("\nMessage on topic: '{topic}' with payload:\n{payload}\n".format(topic=message.topic,payload=message.payload.decode()))
        try:
            #active = json.loads(message.payload.decode())['value']
            active = message.payload.decode()
        except:
            print('Error: Message type not supported!')
            active = "False"
        ledSwitch(active)
        
    def on_connect(client, userdata, flags, rc):
        print("connected with result code {0}".format(str(rc)))
        
    def on_disconnect(client, userdata, rc):
        print("Disconnect, reason: " + str(rc))
        print("Disconnect, reason: " + str(client))
        
    def ledSwitch(isActive):
        global oldval

        if isActive == "True" and oldval == 0:
            oldval = 1
            GPIO.output(33,GPIO.HIGH)
            #print('emer LED on')
            client.publish(topic2, "(is-on emerled1)", 2)
        elif isActive == "False" and oldval == 1:
            oldval = 0
            GPIO.output(33, GPIO.LOW)
            #print('emer LED off')
            client.publish(topic2, "(not(is-on emerled1))", 2)

    client = mqtt.Client('Emergency LED')
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host, 1883, 60)
    client.subscribe(topic, qos=2)
    client.loop_forever()
    
except KeyboardInterrupt:
    print("\nKeyboardInterrupt")
except:
    print("\nOther error or exception")
finally:
    print("\nCleaning up GPIO pins")
    # cleanup resets all GPIO pins   
    GPIO.cleanup()