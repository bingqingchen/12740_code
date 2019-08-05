#!/usr/bin/python
import paho.mqtt.client as mqtt
import sys
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import RPi.GPIO as GPIO

class Device(mqtt.Client):
    def __init__(self, username, password, sensorList, actuatorList):
        super(Device, self).__init__()
        self.host = "mqtt.openchirp.io"
        self.port = 8883
        self.keepalive = 60
        self.username = username
        self.password = password
        
        self.sensors = sensorList
        self.actuators = actuatorList
        
        # Set access credential
        self.username_pw_set(username,password) #set username and pass
        self.tls_set(ca_certs = '/etc/ssl/certs')
        
        # Connect to the Broker, i.e. the OpenChirp server
        self.connect_async(self.host, self.port, self.keepalive)
        self.loop_start()
    
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    def on_connect(self, client, userdata, flags, rc):
        for sensor in self.sensors:
            self.subscribe("openchirp/device/"+self.username+"/"+ sensor)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print('\n' + msg.topic+" "+str(msg.payload.decode()))
        #self.message = msg.payload.decode()

    def on_publish(self, client, userdata, result):
        print("data published")

def main():
    # Modify here based on your own device
    username = '5d488468466cc60c381e0b5e' # Device ID
    password = 'D1vmt0VIWDiVfTvoxn7rnGBMrgCZEO7a' # Token
    sensorList = ['light-dependent_resistor']
    actuatorList = ['light']
    
    # Instantiate your own device
    smart_light = Device(username, password, sensorList, actuatorList)
    
    threshold = 2
    while True:
        sensor_reading = smart_light.subscribe
        if sensor_reading > threshold:
            smart_light.publish() # Turn Light On
        else:
            smart_light.publish() # Turn Light Off

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)



