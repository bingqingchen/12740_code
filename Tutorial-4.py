#!/usr/bin/python
import sys
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import RPi.GPIO as GPIO

import paho.mqtt.client as mqtt

class Device(mqtt.Client):
    def __init__(self, username, password):
        super(Device, self).__init__()
        self.host = "mqtt.openchirp.io"
        self.port = 8883
        self.keepalive = 300
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
        print("Data published")

# Modify here based on your own device
username = '5d488468466cc60c381e0b5e' # Use Device ID as Username
password = 'D1vmt0VIWDiVfTvoxn7rnGBMrgCZEO7a' # Use Token as Password

# Instantiate your own device
smart_light = Device(username, password)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

# Create an MCP3008 object
mcp = MCP.MCP3008(spi, cs)
# Create an analog input channel on the MCP3008 pin 0
channel = AnalogIn(mcp, MCP.P0)

# Set up GPIO for LED
GPIO.setmode(GPIO.BCM)
red_led = 18
GPIO.setup(red_led, GPIO.OUT)

def main():
    # threshold = 2 # Threshold for turn on/off LED
    sensor = "light-dependent_resistor"
    actuator = "light"
    
    # Initialize
    smart_light.device_state[sensor] = 0
    smart_light.device_state[actuator] = 0
    
    while True:
        # Actuate the LED based on command
        GPIO.output(red_led, int(smart_light.device_state[actuator]))
        
        # Read from sensor
        sensor_reading = channel.voltage
        print(sensor_reading)
        smart_light.publish("openchirp/device/"+username+"/"+sensor, payload=sensor_reading, qos=0, retain=True)
        # Save readings
        smart_light.device_state[sensor] = sensor_reading
        
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)



