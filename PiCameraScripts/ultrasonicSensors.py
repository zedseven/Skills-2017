import math
import time
import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    #print(chr(27) + "[2J")
    print('\n' * 200)

trigger1GPIO = 7 #back
echo1GPIO = 11
gpio.setup(trigger1GPIO, gpio.OUT)
gpio.setup(echo1GPIO, gpio.IN)
trigger2GPIO = 13 #right
echo2GPIO = 15
gpio.setup(trigger2GPIO, gpio.OUT)
gpio.setup(echo2GPIO, gpio.IN)
trigger3GPIO = 12 #front
echo3GPIO = 16
gpio.setup(trigger3GPIO, gpio.OUT)
gpio.setup(echo3GPIO, gpio.IN)
trigger4GPIO = 18 #left
echo4GPIO = 22
gpio.setup(trigger4GPIO, gpio.OUT)
gpio.setup(echo4GPIO, gpio.IN)

#------------------------------------------------------

def getDistance(sensor):
    triggerGPIO = -1
    echoGPIO = -1

    if sensor == 1 or sensor == 'back':
        triggerGPIO = trigger1GPIO
        echoGPIO = echo1GPIO
    elif sensor == 2 or sensor == 'right':
        triggerGPIO = trigger2GPIO
        echoGPIO = echo2GPIO
    elif sensor == 3 or sensor == 'front':
        triggerGPIO = trigger3GPIO
        echoGPIO = echo3GPIO
    elif sensor == 4 or sensor == 'left':
        triggerGPIO = trigger4GPIO
        echoGPIO = echo4GPIO
    
    gpio.output(triggerGPIO, gpio.HIGH)
    time.sleep(0.00001)
    gpio.output(triggerGPIO, gpio.LOW)

    startTime = time.time()
    endTime = time.time()
    
    toTime = time.time()
    while gpio.input(echoGPIO) == 0:
        startTime = time.time()
        if time.time() - toTime > 0.5:
            return -1
    
    toTime = time.time()
    while gpio.input(echoGPIO) == 1:
        endTime = time.time()
        if time.time() - toTime > 0.5:
            return -1
        
    elapsedTime = endTime - startTime
    distance = (elapsedTime * 34000) / 2

    return distance

def readDistance(sensor):
    readCount = 11
    reads = []
    for i in range(readCount):
        found = False
        dist = -1
        while found == False:
            dist = getDistance(sensor)
            time.sleep(0.01)#0.001)
            if dist != -1:
                found = True
        reads.append(dist)
    reads.sort()
    return reads[(math.floor(readCount / 2) + 1) - 1]

while True:
    clear()
    print('Back: ' + str(readDistance(1)) + ' cm')
    print('Right: ' + str(readDistance(2)) + ' cm')
    print('Front: ' + str(readDistance(3)) + ' cm')
    print('Left: ' + str(readDistance(4)) + ' cm')
    print('-------------------------------------')
    time.sleep(0.5)
