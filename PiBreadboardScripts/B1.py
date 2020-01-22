import time
import RPi.GPIO as gpio
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT)
gpio.output(12, 1)
print("Turning on...")
time.sleep(2)
gpio.output(12, 0)
print("Turning off...")

