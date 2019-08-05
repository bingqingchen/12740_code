#!/usr/bin/python
import paho.mqtt.client as mqtt

# Create a Device class
class Device(mqtt.Client):
    def __init__(self, username , password, room):
        super(Device, self).__init__()
        self.host = "mqtt.openchirp.io"
        self.port = 8883
        self.keepalive = 60
        self.username = username
        self.password = password
        cafile = "cacert.pem"          # .pem certification file
        

        self.queue = []     #useless for now

        self.username_pw_set(username,password) #set username and pass
        self.tls_set(cafile) #set .pem file

        self.connect_async(self.host, self.port, self.keepalive)

        self.message = None #will hold the messages

        
        self.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #client.subscribe('#')
        self.subscribe("openchirp/device/"+self.username+"/transducer/occupancy")

        #print('Connected with result code:'+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print('\n' + msg.topic+" "+str(msg.payload.decode()))

        #self.message = msg.topic+" "+str(msg.payload)
        self.message = msg.payload.decode()

    def on_publish(self, client, userdata, result):
        print("data published")

    def return_message(self):
        if self.message:
            return 'room ' + self.room + ' occupancy: '+'<font color="red">' + self.message  + '</font>'+'<br /> '
        else:
            return 'room ' + self.room + ' occupancy: ' + '' +'<br /> '


    def return_occupancy(self):
        if self.message:
            return self.message
        else:
            return '0'

def main():
    smart_light = Device()


if __name__ == '__main__':
    main()


