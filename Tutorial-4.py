#!/usr/bin/python
import paho.mqtt.client as mqtt
import sys
#import busio
#import digitalio
#import board
#import adafruit_mcp3xxx.mcp3008 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn
import time
#import RPi.GPIO as GPIO
import numpy as np

class Device(mqtt.Client):
    def __init__(self, username, password):
        super(Device, self).__init__()
        self.host = "mqtt.openchirp.io"
        self.port = 8883
        self.keepalive = 6000
        self.username = username
        self.password = password
        
        # Set access credential
        self.username_pw_set(username, password) #set username and pass
        self.tls_set('cacert.pem')
        
        # Create a dictionary to save all transducer states
        self.device_state = dict()
        
        # Connect to the Broker, i.e. the OpenChirp server
        self.connect(self.host, self.port, self.keepalive)
        self.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connection Successful")
        else:
            print("Connection Unsucessful, rc code = {}".format(rc))
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
        self.subscribe("openchirp/device/"+self.username+"/#") # Subscribe to all tranducers

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload.decode()))
        # Save device state
        transducer = msg.topic.split("/")[-1]
        self.device_state[transducer] = msg.payload.decode()

    def on_publish(self, client, userdata, result):
        print("data published")

def main():
    # Modify here based on your own device
    username = '5d488468466cc60c381e0b5e' # Use Device ID as Username
    password = 'D1vmt0VIWDiVfTvoxn7rnGBMrgCZEO7a' # Use Token as Password
    
    # Instantiate your own device
    smart_light = Device(username, password)#, sensorList, actuatorList)
    
    while True:
        sensor_reading = np.random.rand()
        print(sensor_reading)
        time.sleep(1)
        smart_light.publish("openchirp/device/"+username+"/light-dependent_resistor", payload=sensor_reading, qos=0, retain=True)
        smart_light
    '''
    threshold = 2
    while True:
        sensor_reading = smart_light.subscribe
        if sensor_reading > threshold:
            smart_light.publish() # Turn Light On
        else:
            smart_light.publish() # Turn Light Off
    '''
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)



