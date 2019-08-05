import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import RPi.GPIO as GPIO

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)

# Create an MCP3008 object
mcp = MCP.MCP3008(spi, cs)
# Create an analog input channel on the MCP3008 pin 0
channel = AnalogIn(mcp, MCP.P0)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
red_led = 18
GPIO.setup(red_led, GPIO.OUT)

threshold = 2 # Threshold for turn on/off LED

def main():
    while True:
        if channel.voltage>=threshold:
            GPIO.output(red_led, GPIO.HIGH)
        else:
            GPIO.output(red_led, GPIO.HIGH)
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)

