import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

red_led = 18
button = 25

GPIO.setup(button, GPIO.IN)
GPIO.setup(red_led, GPIO.OUT)

while True:
    if GPIO.input(button):
        GPIO.output(red_led, GPIO.LOW)
    else:
        GPIO.output(red_led, GPIO.HIGH)



