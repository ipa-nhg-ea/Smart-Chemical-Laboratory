#!/usr/bin/python3.7
import Adafruit_DHT
import time
import paho.mqtt.client as mqtt
from datetime import datetime
#import json

# compare bool
oldval = -1

# mqtt
topic1 = "iot/sensors/temperature"
topic2 = "iot/sensors/humidity"
topic3 = "iot/pddl/tempStatus"
host = "192.168.178.20"
localhost = "127.0.0.1"

# time interval
interval = 1

#threshold
threshold = 30

# sensor settings
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# mqtt
def on_connect(client, userdata, flags, rc):
        print("connected with result code {0}".format(str(rc)))

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))
    
def temp_send():
    global oldval
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    #client.publish(topic1, temperature, 2)
    try:
        if humidity is not None and temperature is not None:
            if temperature >= threshold and oldval == 0:
                oldval = 1
                #print("temperature >= threshold")
                client.publish(topic3, "(is-true tempcrit1)", 2)
            elif temperature < threshold and oldval == 1:
                oldval = 0
                #print("temperature < threshold")
                client.publish(topic3, "(not(is-true tempcrit1))", 2)
            elif oldval == -1:
                #print("temp init")
                oldval = 0
                client.publish(topic3, "(not(is-true tempcrit1))", 2)
    except:
        print("Temp./Hum.-Sensor Failure!")
    
client = mqtt.Client('Temperature & Humidity')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host, 1883, 60)
client.loop_start()

while True:
    
    temp_send()
    
    time.sleep(interval);
