#!/usr/bin/python3.7
import requests
import json
import paho.mqtt.client as mqtt

# time interval
interval = 10

# mqtt
topic = "iot/telegram"
host = "192.168.178.20"
localhost = "127.0.0.1"

# mqtt
def on_message(client, userdata, message):
    #print("\nMessage on topic: '{topic}' with payload:\n{payload}\n".format(topic=message.topic,payload=message.payload.decode()))
    try:
        #msg = json.loads(message.payload.decode())
        #print('on_message values:\n', msg)
        msg = message.payload.decode()
        send_message(msg)
    except:
        print('Telegram: Could not decode message.')

# telegram
def send_message(msg):
    # Bot Auth Token
    token = '1815696591:AAF9wNaC6ue0JoU2Xt8yUhe_S6eWfYG44qo'
    sendUrl = f'https://api.telegram.org/bot{token}/sendMessage'
    # IoT Group chat ID
    chat_id = '-456844563'
    #message = 'Message:\n{}'
    try:
        #message = msgBeautify(msg)
        message = msg
    except:
        print('msgBeautify failed.')
    data = {'chat_id': {chat_id}, 'text': {message.format(msg)}}
    requests.post(sendUrl, data).json()
    
def msgBeautify(msg):
    msgType = msg['type']
    msgTs = msg['timestamp']
    msgVal = msg['value']
    niceMsg = "Device: '{type}'\nValue:   '{val}'\nTime:    '{ts}'".format(type=msgType, val=msgVal, ts=msgTs)
    return niceMsg

# mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(str(rc)))

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))

if __name__ == '__main__':
    client = mqtt.Client('Telegram')
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host, 1883, 60)
    client.subscribe(topic, 2)
    client.loop_forever()