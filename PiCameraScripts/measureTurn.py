import time
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
forwardGPIO = 29
gpio.setup(forwardGPIO, gpio.OUT, initial=gpio.LOW)
backwardGPIO = 31
gpio.setup(backwardGPIO, gpio.OUT, initial=gpio.LOW)
leftGPIO = 33
gpio.setup(leftGPIO, gpio.OUT, initial=gpio.LOW)
rightGPIO = 35
gpio.setup(rightGPIO, gpio.OUT, initial=gpio.LOW)
pickupGPIO = 37
gpio.setup(pickupGPIO, gpio.OUT, initial=gpio.LOW)


##gpio.output(forwardGPIO, 1)
##time.sleep(3)
##gpio.output(forwardGPIO, 0)
##time.sleep(3)
##gpio.output(backwardGPIO, 1)
##time.sleep(3)
##gpio.output(backwardGPIO, 0)
##time.sleep(3)
##gpio.output(leftGPIO, 1)
##time.sleep(3)
##gpio.output(leftGPIO, 0)
##time.sleep(3)
##gpio.output(rightGPIO, 1)
##time.sleep(3)
##gpio.output(rightGPIO, 0)
##time.sleep(3)
##gpio.output(pickupGPIO, 1)
##time.sleep(3)
##gpio.output(pickupGPIO, 0)
##time.sleep(3)

while True:
    gpio.output(leftGPIO, 1)

gpio.output(forwardGPIO, gpio.LOW)
gpio.output(backwardGPIO, gpio.LOW)
gpio.output(leftGPIO, gpio.LOW)
gpio.output(rightGPIO, gpio.LOW)
gpio.output(pickupGPIO, gpio.LOW)

##right - 
##forwards
##left
##backwards
