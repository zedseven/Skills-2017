import time
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpioPins = [29, 31, 33, 35, 37]
gpioPin0 = 29
gpioPin1 = 31
gpioPin2 = 33
##while True:
##    for p in range(len(gpioPins)):
##        gpio.setup(gpioPins[p], gpio.OUT, initial=gpio.LOW)
##        gpio.output(gpioPins[p], 1)
##        time.sleep(0.5)
##        gpio.output(gpioPins[p], 0)
##        time.sleep(0.5)
##while True:
##    gpio.setup(gpioPin0, gpio.OUT, initial=gpio.LOW)
##    gpio.output(gpioPin0, 1)
##    time.sleep(0.5)
##    gpio.output(gpioPin0, 0)
##    time.sleep(0.5)
gpio.setup(gpioPin0, gpio.OUT, initial=gpio.LOW)
gpio.setup(gpioPin1, gpio.OUT, initial=gpio.LOW)
gpio.setup(gpioPin2, gpio.OUT, initial=gpio.LOW)
while True:
    gpio.output(gpioPin0, 0)
    time.sleep(1)
    gpio.output(gpioPin0, 1)
    gpio.output(gpioPin1, 1)
    gpio.output(gpioPin2, 1)
    time.sleep(1)
    gpio.output(gpioPin1, 0)
    time.sleep(1)
    gpio.output(gpioPin0, 1)
    gpio.output(gpioPin1, 1)
    gpio.output(gpioPin2, 1)
    time.sleep(1)
    gpio.output(gpioPin2, 0)
    time.sleep(1)
    gpio.output(gpioPin0, 1)
    gpio.output(gpioPin1, 1)
    gpio.output(gpioPin2, 1)
    time.sleep(1)
