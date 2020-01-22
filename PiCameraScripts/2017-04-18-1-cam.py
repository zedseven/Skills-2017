##from picamera import PiCamera
##from time import sleep
##
##camera = PiCamera()
##
##print(camera.resolution)
##camera.resolution = (64, 64)
##camera.start_preview()
##sleep(10)
##camera.stop_preview()

##import time
##import picamera
##import picamera.array
##
##with picamera.PiCamera() as camera:
##    camera.framerate = 4
##    camera.resolution = (64, 64)
##    camera.start_preview()
##    time.sleep(2)
##    with picamera.array.PiRGBArray(camera) as stream:
##        camera.capture(stream, format='rgb')#'bgr')
##        image = stream.array
##        for i in range(4):
##            for y in range(len(image)):
##                for x in range(len(image[y])):
##                    if x % 4 == i and y % 4 == i:
##                        #print("(" + str(x) + ", " + str(y) + "): " + str(image[y][x]))
##                        #139, 69, 19
##                        r = image[y][x][0]
##                        g = image[y][x][1]
##                        b = image[y][x][2]
##                        if r >= 120 and r < 160 and g >= 50 and g < 90 and b >= 0 and b < 40:
##                            print("This pixel is brown!")

##import pygame, sys, math
##from pygame.locals import *
##import time
##import picamera
##import picamera.array
##sys.setrecursionlimit(100000)
##res = (64, 64)
##
##pygame.init()
##screen = pygame.display.set_mode((res[0]*8, res[1]*8))
##pygame.draw.rect(screen, (100, 100, 100), (0, 0, 4, 4), 0)
##
##checked = []
##checkCoords = []
##
##def checkPixel(coords):
##    #print("Analyzing " + str(coords))
##    global image
##    global checked
##    global checkCoords
##    global brown
##    global brownBuffer
##    #print("Length of checked: " + str(len(checked)))
##    if coords not in checked:
##        checked.append(coords)
##        #print(str(coords) + " has not been checked!")
##        r = image[coords[1]][coords[0]][0]
##        g = image[coords[1]][coords[0]][1]
##        b = image[coords[1]][coords[0]][2]
##        if r >= brown[0] - brownBuffer and r < brown[0] + brownBuffer and g >= brown[1] - brownBuffer and g < brown[1] + brownBuffer and b >= brown[2] - brownBuffer and brown[2]  + brownBuffer:
##            #print(str(coords) + " is brown!")
##            pygame.draw.ellipse(screen, (255 - r, 255 - g, 255 - b), (coords[0] * drawToScreenPs, coords[1] * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##            pygame.display.update()
##            if coords[0] > 0:
##                #print(str((coords[0] - 1, coords[1])) + " is being called!")
##                checkCoords.append((coords[0] - 1, coords[1]))
##            if coords[0] < res[0] - 1:
##                #print(str((coords[0] + 1, coords[1])) + " is being called!")
##                checkCoords.append((coords[0] + 1, coords[1]))
##            if coords[1] > 0:
##                #print(str((coords[0], coords[1] - 1)) + " is being called!")
##                checkCoords.append((coords[0], coords[1] - 1))
##            if coords[1] < res[1] - 1:
##                #print(str((coords[0], coords[1] + 1)) + " is being called!")
##                checkCoords.append((coords[0], coords[1] + 1))
##        else:
##            pygame.draw.ellipse(screen, (0, 255, 0), (coords[0] * drawToScreenPs, coords[1] * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##            pygame.display.update()
##    else:
##        pygame.draw.ellipse(screen, (255, 0, 0), (coords[0] * drawToScreenPs, coords[1] * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##        pygame.display.update()
##        
##    
##    checkCoords.remove(coords)
##    if len(checkCoords) > 0:
##        checkPixel(checkCoords[0])
##
##with picamera.PiCamera() as camera:
##    dark = 0
##    darkMultiplier = 0.55
##    
##    camera.framerate = 30
##    camera.resolution = res
##    camera.vflip = 1;
##    modulo = 8
##    drawToScreenPs = 8
##    brownBuffer = 20
##    brown = (84, 61, 42)#(139, 69, 19)
##
##    if dark == 1:
##        brown = (round(brown[0] * darkMultiplier), round(brown[1] * darkMultiplier), round(brown[2] * darkMultiplier))
##    
##    #camera.start_preview()
##    time.sleep(2)
##    i = 0
##    I = 0
##    while 1 == 1:
##        with picamera.array.PiRGBArray(camera) as stream:
##            camera.capture(stream, format='rgb')#'bgr')
##            image = stream.array
##            for y in range(len(image)):
##                for x in range(len(image[y])):
##                    r = image[y][x][0]
##                    g = image[y][x][1]
##                    b = image[y][x][2]
##                    #print(str(image[y][x]))
##                    pygame.draw.rect(screen, (r, g, b), (x * drawToScreenPs, y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 0)
##                    coords = (x, y)
##                    if x % modulo == i and y % modulo == I:
##                        checkCoords.append(coords)
##                        checkPixel(coords)
##        pygame.display.update()
##        print("Update...")
##        i += 1
##        if i >= modulo:
##            i = 0
##            I += 1
##        if I >= modulo:
##            I = 0
##        checked = []


#Name: Zacchary Dempsey-Plante (zaccharydempseyplante.ca)
#Started: 2016-10-18
#Description: A script that makes use of the Raspberry Pi Camera to look for
#   miniature footballs, find them, identify them, and navigate a robot towards
#   them to pick them up.
#Written for: The 2017 Skills Canada Robotics Club competition.
#Python version: 3.4.2

import pygame, sys, math
from pygame.locals import *
from datetime import datetime, timedelta
import time
#import random
import picamera
import picamera.array
import RPi.GPIO as gpio

#define constants & shortcuts
math.inf = float('inf')
true = True
false = False

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
forwardGPIO = 29
gpio.setup(forwardGPIO, gpio.OUT, initial=gpio.LOW) #0
backwardGPIO = 31
gpio.setup(backwardGPIO, gpio.OUT, initial=gpio.LOW) #1
leftGPIO = 33
gpio.setup(leftGPIO, gpio.OUT, initial=gpio.LOW) #2
rightGPIO = 35
gpio.setup(rightGPIO, gpio.OUT, initial=gpio.LOW) #3
pickupGPIO = 37
gpio.setup(pickupGPIO, gpio.OUT, initial=gpio.LOW)
#gpioPins = [29, 31, 33, 35, 37]
#for p in range(len(gpioPins)):
#    gpio.setup(gpioPins[p], gpio.OUT, initial=gpio.LOW)
#    gpio.output(gpioPins[p], 1)
#    time.sleep(0.5)
#    gpio.output(gpioPins[p], 0)

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

startGPIO = 40
gpio.setup(startGPIO, gpio.IN)

res = (128, 64)

hasHead = False
verbose = 1 #scale of 0-4, where 0 is none and 4 is ridiculous

if hasHead == True:
    pygame.init()
    pygame.display.set_caption('MiniFootball Detection Feed', 'Cam Feed')
    screen = pygame.display.set_mode((res[0]*8, res[1]*8))
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, 4, 4), 0)

#def printv(value, vLevel):
#    if verbose >= vLevel:
#        print(value)
#    pass

class Coord:
    __coord = (0, 0)
    #property that exposes coord[0] by an easier means.
    def get_x(self):
        return self.__coord[0]
    def set_x(self, x):
        self.__coord = (x, self.__coord[1])
        self.recalcCID()
    x = property(get_x, set_x)
    #property that exposes coord[1] by an easier means.
    def get_y(self):
        return self.__coord[1]
    def set_y(self, y):
        self.__coord = (self.__coord[0], y)
        self.recalcCID()
    y = property(get_y, set_y)
    
    cid = '#X/X' #unique coord identifier
    ref = 'none' #for finding cluster sources
    
    def recalcCID(self):
        self.cid = '#' + str(self.__coord[0]) + '/' + str(self.__coord[1])
    
    def __init__(self, x, y, ref = 'none'):
        self.__coord = (x, y)
        self.recalcCID()
        self.ref = ref

class Cluster:
    cidList = [] #list of associated CIDs
    refList = [] #list of associated ref attributes - for ref-chaining
    
    clid = '#XXXX' #cluster ID
    compiled = False #for checking to see if the other clusters have already been collapsed into it
    absorbedBy = 'none' #cluster that absorbed it - for calculations
    
    def get_size(self):
        return len(self.cidList)
    def set_size(self):
        return False
    size = property(get_size, set_size) #returns the cluster's total size in pixels
    
    def get_pos(self):
        totalPos = (0, 0)
        countAdded = 0
        for d in range(len(self.cidList)):
            cx = int(self.cidList[d][1:].split('/')[0])
            cy = int(self.cidList[d][1:].split('/')[1])
            totalPos = (totalPos[0] + cx, totalPos[1] + cy)
            countAdded += 1
        if countAdded > 0:
            return (int(totalPos[0] / countAdded), int(totalPos[1] / countAdded))
        else:
            return False   
    def set_pos(self):
        return False
    pos = property(get_pos, set_pos) #returns the cluster's position (average of all included pixels' positions - heavy call)
    
    def appendCoord(self, nCid, nRef):
        if nCid not in self.cidList: #prevents duplicates
            self.cidList.append(nCid)
            self.refList.append(nRef)
        
    def absorbCluster(self, cluster): #combines two clusters. NOTE: THE ABSORBED CLUSTER STILL NEEDS TO BE DELETED/REMOVED AFTERWARDS
        self.cidList = self.cidList + cluster.cidList
        self.refList = self.refList + cluster.refList
        
    def genCLID(self):
        global totalClusterCount
        totalClusterCount += 1
        return '#' + str(totalClusterCount - 1).zfill(4) #the -1 is to counterract the line above
        
    def __init__(self, nCidList, nRefList = []):
        self.clid = self.genCLID()
        self.cidList = nCidList
        self.refList = nRefList

checked = []
checkCoords = []
totalClusterCount = 0
clusters = [] #an array of arrays. each array is a cluster.
class States:
    StartCap, Start, Footballs, Endzone, EndCap = range(5)
currentState = States.StartCap
routeList = []
routeIndex = -2
retrieveCount = 0
notFoundCount = 0

def calcCID(x, y):
    return '#' + str(x) + '/' + str(y)

##def checkPixel(coords):
##    global hasHead
##    #printv("Analyzing " + str(coords), 2)
##    global image
##    global checked
##    global checkCoords
##    global clusters
##    global brown
##    global brownBuffer
##    global green
##    global greenBuffer
##    global greenPixelCount
##    #printv("Length of checked: " + str(len(checked)), 4)
##    if coords.cid + ' : ' + coords.ref + ' : 0' not in checked and coords.cid + ' : ' + coords.ref + ' : 1' not in checked:
##        checked.append(coords.cid + ' : ' + coords.ref + ' : 0')
##        checkedIndex = len(checked) - 1
##        #printv(str(coords) + " has not been checked!", 3)
##        cx = coords.x
##        cy = coords.y
##        
##        r = int(image[cy][cx][0])
##        g = int(image[cy][cx][1])
##        b = int(image[cy][cx][2])
##        
##        total = r + g + b
##        ratio = ((r / total if r != 0 else 0), (g / total if g != 0 else 0), (b / total if b != 0 else 0))
##        #print('rgb: (' + str(r) + ', ' + str(g) + ', ' + str(b) + '); total: ' + str(total) + '; ratio: ' + str(ratio))
##        #if r >= brown[0] - brownBuffer and r < brown[0] + brownBuffer and g >= brown[1] - brownBuffer and g < brown[1] + brownBuffer and b >= brown[2] - brownBuffer and b < brown[2] + brownBuffer:
##        if ratio[0] >= brown[0] - brownBuffer and ratio[0] < brown[0] + brownBuffer and ratio[1] >= brown[1] - brownBuffer and ratio[1] < brown[1] + brownBuffer and ratio[2] >= brown[2] - brownBuffer and ratio[2] < brown[2] + brownBuffer:
##            #printv(str(coords) + " is brown!", 3)
##            cSplit = checked[checkedIndex].split(' : ')
##            checked[checkedIndex] = cSplit[0] + ' : ' + cSplit[1] + ' : 1'
##            if hasHead == True:
##                #pygame.draw.ellipse(screen, (255 - r, 255 - g, 255 - b), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##                pygame.draw.ellipse(screen, (255, 0, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##                pygame.display.update()
##            if cx > 0:
##                #printv(str((coords.x - 1, coords.y)) + " is being called!", 4)
##                checkCoords.append(Coord(cx - 1, cy, coords.cid))
##            if cx < res[0] - 1:
##                #printv(str((coords.x + 1, coords.y)) + " is being called!", 4)
##                checkCoords.append(Coord(cx + 1, cy, coords.cid))
##            if cy > 0:
##                #printv(str((coords.x, coords.y - 1)) + " is being called!", 4)
##                checkCoords.append(Coord(cx, cy - 1, coords.cid))
##            if cy < res[1] - 1:
##                #printv(str((coords.x, coords.y + 1)) + " is being called!", 4)
##                checkCoords.append(Coord(cx, cy + 1, coords.cid))
##        elif ratio[0] >= green[0] - greenBuffer and ratio[0] < green[0] + greenBuffer and ratio[1] >= green[1] - greenBuffer and ratio[1] < green[1] + greenBuffer and ratio[2] >= green[2] - greenBuffer and ratio[2] < green[2] + greenBuffer:
##            greenPixelCount += 1
##            if hasHead == True:
##                pygame.draw.ellipse(screen, (255, 255, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##                pygame.display.update()
##        else:
##            if hasHead == True:
##                pygame.draw.ellipse(screen, (0, 255, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##                pygame.display.update()
##    #else:
##    #    if hasHead == True:
##    #        pygame.draw.ellipse(screen, (255, 0, 0), (coords.x * drawToScreenPs, coords.y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##    #        pygame.display.update()
##        
##    checkCoords.remove(coords)
##    #if len(checkCoords) > 0:
##    #    checkPixel(checkCoords[0])

def checkPixel(rCoords):
    global hasHead
    #printv("Analyzing " + str(coords), 2)
    global image
    global checked
    global checkCoords
    global clusters
    global brown
    global brownBuffer
    global green
    global greenBuffer
    global greenPixelCount
    #rCoords format: x + ' : ' + y + ' : ' + ref
    rSplit = rCoords.split(' : ')
    rCID = calcCID(rSplit[0], rSplit[1])
    rCheckM = rSplit[0] + ' : ' + rSplit[1] + ' : '
    #printv("Length of checked: " + str(len(checked)), 4)
##    if coords.cid + ' : ' + coords.ref + ' : 0' not in checked and coords.cid + ' : ' + coords.ref + ' : 1' not in checked:
    if rCheckM + '0' not in checked and rCheckM + '1' not in checked:
        checked.append(rCheckM + '0')
        checkedIndex = len(checked) - 1
        checked.append(rSplit[2])
        #printv(str(coords) + " has not been checked!", 3)
##        coords = Coord(rSplit[0], rSplit[1], rSplit[2])
        
        cx = int(rSplit[0])#coords.x
        cy = int(rSplit[1])#coords.y
        
        r = int(image[cy][cx][0])
        g = int(image[cy][cx][1])
        b = int(image[cy][cx][2])
        
        total = r + g + b
        ratio = ((r / total if r != 0 else 0), (g / total if g != 0 else 0), (b / total if b != 0 else 0))
        #print('rgb: (' + str(r) + ', ' + str(g) + ', ' + str(b) + '); total: ' + str(total) + '; ratio: ' + str(ratio))
        #if r >= brown[0] - brownBuffer and r < brown[0] + brownBuffer and g >= brown[1] - brownBuffer and g < brown[1] + brownBuffer and b >= brown[2] - brownBuffer and b < brown[2] + brownBuffer:
        if ratio[0] >= brown[0] - brownBuffer and ratio[0] < brown[0] + brownBuffer and ratio[1] >= brown[1] - brownBuffer and ratio[1] < brown[1] + brownBuffer and ratio[2] >= brown[2] - brownBuffer and ratio[2] < brown[2] + brownBuffer:
            #printv(str(coords) + " is brown!", 3)
            cSplit = checked[checkedIndex].split(' : ')
            checked[checkedIndex] = cSplit[0] + ' : ' + cSplit[1] + ' : 1'
            if hasHead == True:
                #pygame.draw.ellipse(screen, (255 - r, 255 - g, 255 - b), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.draw.ellipse(screen, (255, 0, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.display.update()
            c1 = str(cx - 1) + ' : ' + str(cy)
            c2 = str(cx + 1) + ' : ' + str(cy)
            c3 = str(cx) + ' : ' + str(cy - 1)
            c4 = str(cx) + ' : ' + str(cy + 1)
            if cx > 0 and c1 + ' : 0' not in checked and c1 + ' : 1' not in checked:
                #printv(str((coords.x - 1, coords.y)) + " is being called!", 4)
                checkCoords.append(c1 + ' : ' + rCID)
            if cx < res[0] - 1 and c2 + ' : 0' not in checked and c2 + ' : 1' not in checked:
                #printv(str((coords.x + 1, coords.y)) + " is being called!", 4)
                checkCoords.append(c2 + ' : ' + rCID)
            if cy > 0 and c3 + ' : 0' not in checked and c3 + ' : 1' not in checked:
                #printv(str((coords.x, coords.y - 1)) + " is being called!", 4)
                checkCoords.append(c3 + ' : ' + rCID)
            if cy < res[1] - 1 and c4 + ' : 0' not in checked and c4 + ' : 1' not in checked:
                #printv(str((coords.x, coords.y + 1)) + " is being called!", 4)
                checkCoords.append(c4 + ' : ' + rCID)
        elif ratio[0] >= green[0] - greenBuffer and ratio[0] < green[0] + greenBuffer and ratio[1] >= green[1] - greenBuffer and ratio[1] < green[1] + greenBuffer and ratio[2] >= green[2] - greenBuffer and ratio[2] < green[2] + greenBuffer:
            greenPixelCount += 1
            if hasHead == True:
                pygame.draw.ellipse(screen, (255, 255, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.display.update()
        else:
            if hasHead == True:
                pygame.draw.ellipse(screen, (0, 255, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.display.update()
    #else:
    #    if hasHead == True:
    #        pygame.draw.ellipse(screen, (255, 0, 0), (coords.x * drawToScreenPs, coords.y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
    #        pygame.display.update()
        
    checkCoords.remove(rCoords)
    #if len(checkCoords) > 0:
    #    checkPixel(checkCoords[0])

def findConnectedClusters(c):
    for d in range(len(clusters[c].cidList)):
        #if killIteration == False:
        if clusters[c].cidList[d] not in clusters[c].refList: #outermost coordinate - if not used anywhere else, it is along the border
            cx = int(clusters[c].cidList[d][1:].split('/')[0])
            cy = int(clusters[c].cidList[d][1:].split('/')[1])
            if hasHead == True:
                pygame.draw.ellipse(screen, (255, 0, 255), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.display.update()
                #time.sleep(0.01)
            #otherClustersRange = list(range(len(clusters)))
            #otherClustersRange.reverse()
            for o in range(len(clusters)):#otherClustersRange:
                #O = (len(clusters) - 1) - o
                if o != c: #every OTHER cluster
                    mergeClusters = False
                    if mergeClusters == False and calcCID(cx - 1, cy) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx + 1, cy) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx, cy - 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx, cy + 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx - 1, cy - 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx - 1, cy + 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx + 1, cy + 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == False and calcCID(cx + 1, cy - 1) in clusters[o].cidList:
                        mergeClusters = True
                    if mergeClusters == True:
                        if clusters[o].absorbedBy == 'none' and clusters[c].absorbedBy != clusters[o].clid:
                            clusters[o].absorbedBy = clusters[c].clid
                        #clusters[c].absorbCluster(clusters[o])
                        #clusters.pop(o)


def findClusterByID(clid):
    for c in range(len(clusters)):
        if clusters[c].clid == clid:
            return c
    return -1

def findClustersAbsorbedBy(clid):
    absorbedClusters = []
    for c in range(len(clusters)):
        if clusters[c].absorbedBy == clid:
            absorbedClusters.append(clusters[c].clid)
    return absorbedClusters

def compileCluster(clid):
    searchClusters = findClustersAbsorbedBy(clid)
    print(searchClusters)
    searchRange = list(range(len(searchClusters)))
    searchRange.reverse()
    for s in searchRange:
        searchCluster = clusters[findClusterByID(searchClusters[s])]
        if searchCluster.compiled == False:
            compileCluster(searchClusters[s])
        clusters[findClusterByID(clid)].absorbCluster(searchCluster)
        clusters.remove(searchCluster)
    clusters[findClusterByID(clid)].compiled = True

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
    distance = (elapsedTime * 34029) / 2

    if distance < 0 or distance >= 2500:
        distance = 0
    
    return distance

def readDistance(sensor):
    readCount = 5
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
##    print('Read! ' + str(reads[(math.floor(readCount / 2) + 1) - 1]))
    return reads[(math.floor(readCount / 2) + 1) - 1]

def nameGPIO(gpio):
    global forwardGPIO
    global backwardGPIO
    global leftGPIO
    global rightGPIO
    if gpio == forwardGPIO:
        return 'forward'
    elif gpio == backwardGPIO:
        return 'backward'
    elif gpio == leftGPIO:
        return 'left'
    elif gpio == rightGPIO:
        return 'right'
    elif gpio == pickupGPIO:
        return 'pickup'
    else:
        return 'unknown'

def oppositeGPIO(gpio):
    global forwardGPIO
    global backwardGPIO
    global leftGPIO
    global rightGPIO
    if gpio == forwardGPIO:
        return backwardGPIO
    elif gpio == backwardGPIO:
        return forwardGPIO
    elif gpio == leftGPIO:
        return rightGPIO
    elif gpio == rightGPIO:
        return leftGPIO
    else:
        return gpio

##def move(dirGPIO, movePercent, numChecks, action, actionDir, actionDist):
##    threshold = 1
##    if action == 'hug':
##        actionSensor = actionDir
##        for i in range(numChecks):
##            gpio.output(dirGPIO, 1)
##            time.sleep((movePercent / numChecks) * fullMoveTime)
##            gpio.output(dirGPIO, 0)
##            readDist = readDistance(actionSensor)
##            offAmnt = readDist - actionDist
##            if offAmnt > -threshold and offAmnt < threshold:
##                pass
##            else:
##                adjustGPIO = leftGPIO#(leftGPIO if offAmnt >= 0 else rightGPIO)
##                if actionDir == 'right':
##                    adjustGPIO = oppositeGPIO(adjustGPIO)
##                if offAmnt < 0:
##                    adjustGPIO = oppositeGPIO(adjustGPIO)
##                print(str(offAmnt) + ' : ' + nameGPIO(adjustGPIO))
##                gpio.output(adjustGPIO, 1)
##                time.sleep(fullTurnTime * (1.25 / 360))
##                gpio.output(adjustGPIO, 0)
##    elif action == 'stop':
##        actionSensor = actionDir
##        gpio.output(dirGPIO, 1)
##        found = False
##        while found == False:
##            readDist = readDistance(actionSensor)
##            offAmnt = readDist - actionDist
##            if offAmnt > -threshold and offAmnt < threshold:
##                found = True
##        gpio.output(dirGPIO, 0)
def moveUntil(moveGPIO, moveSensor, moveDist, moveOffPositive):
    gpio.output(moveGPIO, 1)
    #threshold = 1
    stuckCheckCount = 10
    stuckThreshold = 2
    runCount = 0
    correctCount = 0
    prevDist = -1
    found = False
    while found == False:
        readDist = readDistance(moveSensor)
        offAmnt = readDist - moveDist
        #if offAmnt > -threshold and offAmnt < threshold:
        if (moveOffPositive == True and offAmnt <= 0) or (moveOffPositive == False and offAmnt >= 0):
            found = True
            print('Done moving! ' + str(readDist) + ' : ' + str(offAmnt))
            #Brake
            gpio.output(oppositeGPIO(moveGPIO), 1)
            time.sleep(0.2)
            gpio.output(oppositeGPIO(moveGPIO), 0)
        else:
            if runCount % stuckCheckCount == 0:
##                print('Checking to see if we\'re stuck.')
                if prevDist >= 0 and abs(readDist - prevDist) <= stuckThreshold:
                    if correctCount % 2 == 0:
                        print('We\'re stuck, so we\'ll make a minor adjustment.')
                        gpio.output(moveGPIO, 0)
                        gpio.output(oppositeGPIO(moveGPIO), 1)
                        time.sleep(fullMoveTime * 0.2)
                        gpio.output(oppositeGPIO(moveGPIO), 0)
                        gpio.output(leftGPIO, 1)
                        time.sleep(fullTurnTime * (5 / 360))
                        gpio.output(leftGPIO, 0)
                        gpio.output(rightGPIO, 1)
                        time.sleep(fullTurnTime * (5 / 360))
                        gpio.output(rightGPIO, 0)
                        gpio.output(moveGPIO, 1)
                    else:
                        print('We\'re stuck, so we\'ll make a major adjustment.')
                        fixGPIO = (leftGPIO if moveGPIO == backwardGPIO else rightGPIO)
                        gpio.output(moveGPIO, 0)
                        gpio.output(oppositeGPIO(moveGPIO), 1)
                        time.sleep(fullMoveTime * 0.6)
                        gpio.output(oppositeGPIO(moveGPIO), 0)
                        gpio.output(fixGPIO, 1)
                        time.sleep(fullTurnTime * ((11.25 + (correctCount * 2)) / 360))
                        gpio.output(fixGPIO, 0)
                        gpio.output(moveGPIO, 1)
                    correctCount += 1
                prevDist = readDist
        runCount += 1
    gpio.output(moveGPIO, 0)
def hugUntil(moveGPIO, moveSensor, hugSensor, moveDist, hugDist, moveOffPositive, fullMovePercent):
    #moveThreshold = 5
    hugThreshold = 1
    stuckCheckCount = 5
    stuckThreshold = 10
    runCount = 0
    correctCount = 0
    prevDist = -1
    found = False
    while found == False:
        gpio.output(moveGPIO, 1)
        time.sleep(fullMoveTime * fullMovePercent)
        gpio.output(moveGPIO, 0)
        readDist = readDistance(hugSensor)
        offAmnt = readDist - hugDist
        if offAmnt > -hugThreshold and offAmnt < hugThreshold:
            pass
        else:
            adjustGPIO = leftGPIO#(leftGPIO if offAmnt >= 0 else rightGPIO)
            if hugSensor == 'right':
                adjustGPIO = oppositeGPIO(adjustGPIO)
            if offAmnt < 0:
                adjustGPIO = oppositeGPIO(adjustGPIO)
            if moveGPIO == backwardGPIO:
                adjustGPIO = oppositeGPIO(adjustGPIO)
##            print(str(offAmnt) + ' : ' + nameGPIO(adjustGPIO))
            gpio.output(adjustGPIO, 1)
            time.sleep(fullTurnTime * (1.3525 / 360))
            gpio.output(adjustGPIO, 0)
        readDist = readDistance(moveSensor)
        offAmnt = readDist - moveDist
        #if offAmnt > -moveThreshold and offAmnt < moveThreshold:
        if (moveOffPositive == True and offAmnt <= 0) or (moveOffPositive == False and offAmnt >= 0):
            found = True
            print('Hug is done.')
            #Brake
            gpio.output(oppositeGPIO(moveGPIO), 1)
            time.sleep(0.2)
            gpio.output(oppositeGPIO(moveGPIO), 0)
        else:
            if runCount % stuckCheckCount == 0:
##                print('Checking to see if we\'re stuck.')
                if prevDist >= 0 and abs(readDist - prevDist) <= stuckThreshold:
                    if correctCount % 2 == 0:
                        print('We\'re stuck, so we\'ll make a minor adjustment.')
                        gpio.output(moveGPIO, 0)
                        gpio.output(oppositeGPIO(moveGPIO), 1)
                        time.sleep(fullMoveTime * 0.2)
                        gpio.output(oppositeGPIO(moveGPIO), 0)
                        gpio.output(leftGPIO, 1)
                        time.sleep(fullTurnTime * (5 / 360))
                        gpio.output(leftGPIO, 0)
                        gpio.output(rightGPIO, 1)
                        time.sleep(fullTurnTime * (5 / 360))
                        gpio.output(rightGPIO, 0)
                        gpio.output(moveGPIO, 1)
                    else:
                        print('We\'re stuck, so we\'ll make a major adjustment.')
                        fixGPIO = (leftGPIO if moveGPIO == backwardGPIO else rightGPIO)
                        gpio.output(moveGPIO, 0)
                        gpio.output(oppositeGPIO(moveGPIO), 1)
                        time.sleep(fullMoveTime * 0.6)
                        gpio.output(oppositeGPIO(moveGPIO), 0)
                        gpio.output(fixGPIO, 1)
                        time.sleep(fullTurnTime * ((11.25 + (correctCount * 2)) / 360))
                        gpio.output(fixGPIO, 0)
                        gpio.output(moveGPIO, 1)
                    correctCount += 1
                prevDist = readDist
        runCount += 1
##def rightAngleTurn(turnGPIO, turnSensor, smallerToLarger):
##    threshold = 1
##    gpio.output(turnGPIO, 1)
##    found = False
##    stage = 0
##    lastVal = False
##    while found == False:
##        currentVal = readDistance(turnSensor)
##        #if lastVal != False and ((smallerToLarger == True and lastVal < currentVal) or (smallerToLarger == False and lastVal > currentVal)):
##        #    pass
##        if lastVal == False:
##            pass
##        elif stage == 0 and lastVal - currentVal > threshold: #supposed to be getting larger in stage 0
##            stage = 1
##            print('Moving to Stage 1!')
##        elif stage == 1 and lastVal - currentVal < -threshold: #supposed to be getting smaller in stage 1
##            found = True
##            print('Moving to Stage 2!')
##        lastVal = currentVal
##    gpio.output(turnGPIO, 0)
##    #Brake
##    gpio.output(oppositeGPIO(turnGPIO), 1)
##    time.sleep(0.2)
##    gpio.output(oppositeGPIO(turnGPIO), 0)

def captureFrame(camera, stream):
    camera.capture(stream, format='rgb')#'bgr')
    return stream.array

def changeState(newState):
    global currentState
    newStateName = ''
    if newState == States.StartCap:
        newStateName = 'StartCap'
    elif newState == States.Start:
        newStateName = 'Start'
    elif newState == States.Footballs:
        newStateName = 'Footballs'
    elif newState == States.Endzone:
        newStateName = 'Endzone'
    elif newState == States.EndCap:
        newStateName = 'EndCap'
    time.sleep(1)
    print('Changing states to \'' + newStateName + '\'.')
    currentState = newState

with picamera.PiCamera() as camera:
    #picamera.readthedocs.io/en/release-1.10/api_camera.html
    camera.framerate = 30
    camera.resolution = res
    camera.exposure_mode = 'sports' #off, auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    camera.exposure_compensation = 25
    camera.awb_mode = 'flash' #off, auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
    camera.vflip = 1
    camera.hflip = 1
    cameraFOV = (27.5 * 2) #(15 * 2)#27.5° from the center (straight out) to the edge of the view - really anything from 15-20°. (I didn't have a protractor at the time)
    fullMoveTime = 1.7#1.9849081365#2.20#2.30 #time taken to move forward fullMoveDistance in seconds
    fullMoveDistance = 30.0#27.50#30.48 #distance in cm
    fullTurnTime = 6.75#6.5 left, 7 for right#5.6#(2.9 * 2)#4 #time taken to perform a full 360° turn in seconds
    forwardSensitivity = 7 #how close to the center a football must be before going to pick it up
    fullMoveSize = 95#115 #tested with 150
    pickupSize = 1550#1500#1900#2300#1500 #2419 #tested with 2500
    pickupSensitivity = 0.125 #how close to the ideal football screen size a football should be before pickup
    lastGPIO = forwardGPIO
    notFoundMoveTime = 1 #in seconds
    noBrownStuckTime = 60 #in seconds - how long to wait without finding brown before kicking in the failsafe
    modulo = 8
    drawToScreenPs = 8
    brownBuffer = 0.055#0.05#0.02
    brown = (50, 33, 44)#(82, 63, 52)#(113, 97, 92)#(79, 62, 29)#(113, 100, 53)#(83, 64, 27)#(59, 44, 18)#(153, 142, 110)#(128, 90, 62)#(143, 111, 107)#(153, 111, 107)#(79, 80, 79)#(81, 55, 34)#(102, 26, 0)#(115, 98, 103)#(84, 61, 42)#(139, 69, 19)
    brownTotal = brown[0] + brown[1] + brown[2]
    brown = (brown[0] / brownTotal, brown[1] / brownTotal, brown[2] / brownTotal)
    greenBuffer = 0.05#0.02
    green = (0, 116, 92)#(0, 142, 43)
    greenTotal = green[0] + green[1] + green[2]
    green = (green[0] / greenTotal, green[1] / greenTotal, green[2] / greenTotal)
    greenPixelMin = 20 #minimum number of green pixels to have in a capture before acknowledging.
    #perfectWhite = (133, 133, 133)#(122, 126, 81)#(255, 255, 255)
    #print(camera.contrast)
    #if hasHead == True:
        #print("Please put a white piece of paper 1ft in front of the camera to calibrate the brown-colour search. Press enter when ready.")
        #input()fullMoveDistance
##    avgCenterList = []
##    with picamera.array.PiRGBArray(camera) as streamCali:
##            camera.capture(streamCali, format='rgb')#'bgr')
##            imageCali = streamCali.array
##            for y in range(len(imageCali)):
##                for x in range(len(imageCali[y])):
##                    if hasHead == True:
##                        pygame.draw.rect(screen, (imageCali[y][x][0], imageCali[y][x][1], imageCali[y][x][2]), (x * drawToScreenPs, y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 0)
##                    if y > round((res[1] / 2) - 1) - 5 and y < round((res[1] / 2) - 1) + 5:
##                        if x > round((res[0] / 2) - 1) - 5 and x < round((res[0] / 2) - 1) + 5:
##                            if hasHead == True:
##                                pygame.draw.ellipse(screen, (0, 0, 255), (x * drawToScreenPs, y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
##                            avgCenterList.append((imageCali[y][x][0], imageCali[y][x][1], imageCali[y][x][2]))
##                            #print((imageCali[y][x][0], imageCali[y][x][1], imageCali[y][x][2]))
##    if hasHead == True:
##        pygame.display.update()
##    avgTotal = (0, 0, 0)
##    for o in range(len(avgCenterList)):
##        avgTotal = (avgTotal[0] + avgCenterList[o][0], avgTotal[1] + avgCenterList[o][1], avgTotal[2] + avgCenterList[o][2])
##    avgColour = (round(avgTotal[0] / len(avgCenterList)), round(avgTotal[1] / len(avgCenterList)), round(avgTotal[2] / len(avgCenterList)))
    #printv("The average colour is: " + str(avgColour), 1)
    #print(avgColour)
    
    #brown = (round(brown[0] * round(avgColour[0] / perfectWhite[0])), round(brown[1] * round(avgColour[1] / perfectWhite[1])), round(brown[2] * round(avgColour[2] / perfectWhite[2])))
    
    #printv("Brown is " + str(brown), 1)
    #camera.contrast = round((100.0 / ((avgColour[0] + avgColour[1] + avgColour[2]) / 3.0)) * camera.contrast)
    #if hasHead == True:
        #camera.start_preview()
    gpio.output(forwardGPIO, 0)
    gpio.output(backwardGPIO, 0)
    gpio.output(leftGPIO, 0)
    gpio.output(rightGPIO, 0)
    gpio.output(pickupGPIO, 0)
    time.sleep(2)
    lastRunTime = datetime.now()
    thisRunTime = lastRunTime
    deltaTime = None #lastRunTime - thisRunTime
    deltaMillis = None #((deltaTime.days * 24 * 60 * 60 + deltaTime.seconds) * 1000 + deltaTime.microseconds / 1000.0)
    lastTurnDir = 0 #0 for left, 1 for right
    lastBrownTime = thisRunTime
    greenPixelCount = 0
    i = 0
    I = 0
    print('Ready to go; waiting for the signal.')
    while gpio.input(startGPIO) == gpio.LOW:
        pass
    print('Received the signal! We\'re going!')
    while True:
        if currentState == States.StartCap:
##            routeList.append((forwardGPIO, fullMoveTime * 0.75))
            gpio.output(forwardGPIO, 1)
            time.sleep(fullMoveTime * 0.75)
            gpio.output(forwardGPIO, 0)
##            routeList.append((rightGPIO, fullTurnTime * (90 / 360)))
            gpio.output(rightGPIO, 1)
            time.sleep(fullTurnTime * (90 / 360))
            gpio.output(rightGPIO, 0)
##            rightAngleTurn(rightGPIO, 'right', True)
##            routeList.append((forwardGPIO, fullMoveTime * 1))
##            gpio.output(forwardGPIO, 1)
##            time.sleep(fullMoveTime * 1)
##            gpio.output(forwardGPIO, 0)
            moveUntil(forwardGPIO, 'front', 7.5, True)
##            routeList.append((leftGPIO, fullTurnTime * (90 / 360)))
            gpio.output(leftGPIO, 1)
            time.sleep(fullTurnTime * (90 / 360))
            gpio.output(leftGPIO, 0)
            changeState(States.Start)
##            rightAngleTurn(leftGPIO, 'right', True)
        elif currentState == States.Start:
##            routeList.append((forwardGPIO, fullMoveTime * 1.75))
##            gpio.output(forwardGPIO, 1)
##            time.sleep(fullMoveTime * 1.75)
##            gpio.output(forwardGPIO, 0)
            #move(forwardGPIO, fullMoveTime * 20, 60, 'hug', 'right', 6) #1.75x10
            hugUntil(forwardGPIO, 'front', 'right', 50, 7.5, True, 0.2)
##            routeList.append((leftGPIO, fullTurnTime * (25 / 360)))
            gpio.output(leftGPIO, 1)
            time.sleep(fullTurnTime * (90 / 360))
            gpio.output(leftGPIO, 0)
##            rightAngleTurn(leftGPIO, 'left', True)
            moveUntil(backwardGPIO, 'back', 2.5, True)
            moveUntil(forwardGPIO, 'back', (12 + (retrieveCount * 10)), False)
            gpio.output(rightGPIO, 1)
            time.sleep(fullTurnTime * (90 / 360))
            gpio.output(rightGPIO, 0)
##            rightAngleTurn(rightGPIO, 'right', True)
            changeState(States.Footballs)
##            changeState(States.Endzone)
        elif currentState == States.Footballs:
            thisRunTime = datetime.now()
            deltaTime = lastRunTime - thisRunTime
            deltaMillis = ((deltaTime.days * 24 * 60 * 60 + deltaTime.seconds) * 1000 + deltaTime.microseconds / 1000.0)
            
            with picamera.array.PiRGBArray(camera) as stream:
                #camera.capture(stream, format='rgb')#'bgr')
                #image = stream.array
                image = captureFrame(camera, stream)
                for y in range(len(image)):
                    for x in range(len(image[y])):
                        r = image[y][x][0]
                        g = image[y][x][1]
                        b = image[y][x][2]
                        if x == math.floor(res[0] / 2) and y == math.floor(res[1] / 2):
                            print(str(image[y][x]))
                        #printv(str(image[y][x]), 5)
                        if hasHead == True:
                            pygame.draw.rect(screen, (r, g, b), (x * drawToScreenPs, y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 0)
    ##                    coords = Coord(x, y, 'none')
                        if x % modulo == i and y % modulo == I:
                            checkCoords.append(str(x) + ' : ' + str(y) + ' : none')
                        #print('(' + str(x) + ', ' + str(y) + ') : (' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')
                while len(checkCoords) > 0:
                    checkPixel(checkCoords[0])
                print('Handling clusters.')
                #find/create all clusters
                for c in range(len(checked)):
                    if c % 2 == 0:
                        split = checked[c].split(' : ') #receives a string in the format of cid : ref : isBrown
                        cid = calcCID(split[0], split[1]) #format: '#X/Y'
                        ref = checked[c + 1] #can either be 'none' or another cid
                        isBrown = (True if split[2] == '1' else False) #binary - yes or no
                        if isBrown == True:
                            if ref == 'none':
                                clusters.append(Cluster([cid], [ref])) #including the 'none' ref because it keeps the indexing identical from list to list
                            else:
                                for d in range(len(clusters)):
                                    if ref in clusters[d].cidList:
                                        clusters[d].appendCoord(cid, ref)
                                        break
                #combine clusters as necessary
                #killIteration = False
                for c in range(len(clusters)):
                    #if killIteration == False:
                    findConnectedClusters(c)
                                        #killIteration = True
                    #else:
                        #killIteration = False

                #for every cluster, check for other clusters that say they were
                #absorbed by it. check to see if any other clusters were absorbed
                #by the found cluster, and repeat the process. potentially a function.
                for c in range(len(clusters)):
                    print(clusters[c].clid + ' : ' + clusters[c].absorbedBy)
                for n in range(2):
                    if n == 1: #two passes - the first does 90% of the work, but the second ties up small issues such as 1 3 4 2 where the number is the order the clusters are viewed in
                        for c in range(len(clusters)):
                            clusters[c].compiled = False
                        for c in range(len(clusters)):
                            findConnectedClusters(c)
                    compiledAllClusters = False
                    while compiledAllClusters == False:
                        foundUncompiled = False
                        for c in range(len(clusters)):
                            if clusters[c].compiled == False:
                                foundUncompiled = True
                                compileCluster(clusters[c].clid)
                                break
                        if foundUncompiled == False:
                            compiledAllClusters = True
                    
                clusterCount = len(clusters)
                print('There ' + ('are' if clusterCount != 1 else 'is') + ' ' + str(clusterCount) + ' total cluster' + ('s' if clusterCount != 1 else '') + '.')
                if hasHead == True:
                    for c in range(clusterCount):
                        clusterColour = (255 * (0 if clusterCount <= 1 else (1 - (c / (clusterCount - 1)))), 255 * (0 if clusterCount <= 1 else (1 - (c / (clusterCount - 1)))), 255 * (1 if clusterCount <= 1 else (c / (clusterCount - 1))))#(random.randint(127, 255), random.randint(127, 255), random.randint(127, 255))#(0, 0, 255)
                        for d in range(len(clusters[c].cidList)):
                            cx = int(clusters[c].cidList[d][1:].split('/')[0])
                            cy = int(clusters[c].cidList[d][1:].split('/')[1])
                            pygame.draw.ellipse(screen, clusterColour, (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                    pygame.display.update()
                #handle robot navigation °_°
                if clusterCount > 0:
                    lastBrownTime = thisRunTime
                    largestCluster = (-1, 0, math.inf) #(index, size, distance)
                    closestCluster = (-1, 0, math.inf) #(index, size, distance)
                    for c in range(clusterCount):
                        cSize = clusters[c].size
                        cPos = clusters[c].pos #(x, y) - only really interested in the x
                        centerOffset = cPos[0] - int(res[0] / 2)
                        if cSize > largestCluster[1]:
                            largestCluster = (c, cSize, centerOffset)
                        if abs(centerOffset) < abs(closestCluster[2]): #absolute value of (x - center) (we don't really care about y-level closeness
                            closestCluster = (c, cSize, centerOffset)
                    print('The largest cluster is ' + str(largestCluster[0]) + ', with a size of ' + str(largestCluster[1]) + ' pixel' + ('s' if largestCluster[1] != 1 else '') + ' and an x-distance of ' + str(abs(largestCluster[2])) + ' pixel' + ('s' if abs(largestCluster[2]) != 1 else '') + '.')
                    print('The closest cluster is ' + str(closestCluster[0]) + ', with an x-distance of ' + str(abs(closestCluster[2])) + ' pixel' + ('s' if abs(closestCluster[2]) != 1 else '') + ' and a size of ' + str(closestCluster[1]) + ' pixel' + ('s' if closestCluster[1] != 1 else '') + '.')
##                    if closestCluster[1] / largestCluster[1] >= 0.65:
##                        targetCluster = closestCluster
##                    else:# if closestCluster[2] / largestCluster[2]:
##                        targetCluster = largestCluster
                    targetCluster = closestCluster
                    minSize = math.sqrt(fullMoveSize)
                    maxSize = math.sqrt(pickupSize)
                    turnAmnt = (targetCluster[2] / int(res[0] / 2)) * (cameraFOV / 2)
                    turnTime = (0 if turnAmnt == 0 else fullTurnTime * (abs(turnAmnt) / 360))
                    moveAmnt = 1 - ((math.sqrt(targetCluster[1]) - minSize) / (maxSize - minSize))#((targetCluster[1] / pickupSize) / fullMoveDistance)#((targetCluster[1] / pickupSize) / 0.18)# * 30.48 #abs(1 - (targetCluster[1] / pickupSize))
                    moveTime = abs(moveAmnt * (fullMoveTime * (30.0 / fullMoveDistance))) #(fullMoveTime * (15.1 / 14.089))
                    turned = False
                    moved = False
                    if turnAmnt >= forwardSensitivity: #turn right
                        print('Turn ' + str(abs(turnAmnt)) + '° right. (turn right for ' + str(turnTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                        gpio.output(rightGPIO, 1)
                        lastGPIO = rightGPIO
                        routeList.append((rightGPIO, turnTime))
                        turned = True
                    elif turnAmnt <= -forwardSensitivity: #turn left
                        print('Turn ' + str(abs(turnAmnt)) + '° left. (turn left for ' + str(turnTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                        gpio.output(leftGPIO, 1)
                        lastGPIO = leftGPIO
                        routeList.append((leftGPIO, turnTime))
                        turned = True
                    else: #go forward
                        if moveAmnt >= pickupSensitivity:
                            print('Move ' + str(abs(moveAmnt) * fullMoveDistance) + 'cm forwards. (move forwards for ' + str(moveTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                            gpio.output(forwardGPIO, 1)
                            lastGPIO = forwardGPIO
                            routeList.append((forwardGPIO, moveTime))
                            moved = True
                        elif moveAmnt <= -pickupSensitivity:
                            print('Move ' + str(abs(moveAmnt) * fullMoveDistance) + 'cm backwards. (move backwards for ' + str(moveTime) + ' seconds away from cluster ' + str(targetCluster[0]) + ')')
                            gpio.output(backwardGPIO, 1)
                            lastGPIO = backwardGPIO
                            routeList.append((backwardGPIO, moveTime))
                            moved = True
                        else:
                            print('Pick up the football! (displayed as cluster ' + str(targetCluster[0]) + ')')
                            gpio.output(pickupGPIO, 1)
                            #lastGPIO = pickupGPIO
                            changeState(States.Endzone)
                            time.sleep(0.00001)
                    notFoundCount = 0
                    time.sleep((turnTime if turned == True else (moveTime if moved == True else 0.5)))
                    gpio.output(forwardGPIO, 0)
                    gpio.output(backwardGPIO, 0)
                    gpio.output(leftGPIO, 0)
                    gpio.output(rightGPIO, 0)
                    gpio.output(pickupGPIO, 0)
                else:
##                    bTime = lastRunTime - lastBrownTime
##                    bMillis = ((bTime.days * 24 * 60 * 60 + bTime.seconds) * 1000 + bTime.microseconds / 1000.0)
##                    if bMillis >= noBrownStuckTime * 1000:
##                        #if we haven't detected brown in a while, move backward a bit and rotate 90° to the right.
##                        print('We\'re stuck.')
##                        gpio.output(backwardGPIO, 1)
##                        time.sleep(fullMoveTime)
##                        gpio.output(backwardGPIO, 0)
##                        gpio.output(rightGPIO, 1)
##                        time.sleep((90 / 360) * fullTurnTime)
##                        gpio.output(rightGPIO, 0)
##                        lastGPIO = forwardGPIO
##                        lastBrownTime += timedelta(seconds=(noBrownStuckTime / 2))
##                    if greenPixelCount > greenPixelMin:
##                        print('Nothing was found and we saw green, so we\'re going to turn left ~5.625°.')
##                        gpio.output(leftGPIO, 1)
##                        time.sleep((5.625 / 360) * fullTurnTime)
##                        gpio.output(leftGPIO, 0)
##                    else:
                    print('Nothing was found, so we\'re going to see if we can get better.')
                    print(str(fullMoveTime))
                    actGPIO = leftGPIO
                    actTime = 0
                    if notFoundCount <= 5:
                        actGPIO = forwardGPIO
                        actTime = fullMoveTime * 0.5
                    elif notFoundCount == 6:
                        actGPIO = rightGPIO
                        actTime = fullTurnTime * (45 / 360)
                    elif notFoundCount == 7:
                        actGPIO = leftGPIO
                        actTime = fullTurnTime * (22.5 / 360)
                    elif notFoundCount <= 9:
                        actGPIO = leftGPIO
                        actTime = fullTurnTime * (11.25 / 360)
                        routeList.append((backwardGPIO, fullMoveTime * 1))
                        gpio.output(backwardGPIO, 1)
                        time.sleep(fullMoveTime * 1)
                        gpio.output(backwardGPIO, 0)
                    if notFoundCount >= 9:
                        notFoundCount = 0
                    routeList.append((actGPIO, actTime))
                    gpio.output(actGPIO, 1)
                    time.sleep(actTime)
                    gpio.output(actGPIO, 0)
                    notFoundCount = (notFoundCount + 1 if notFoundCount < 5 else 0)
                #allow time for viewing results
                if hasHead == True:
                    time.sleep(0.5)
                print('Done.')
                print('--------------------------------------------------------------------------')
##                if lastGPIO == pickupGPIO:
##                    time.sleep(30)
                
                    #if hasHead == True:
                    #    pygame.display.update()
            #if hasHead == True:
            #    pygame.display.update()
            #printv("Update...", 1)
            i += 1
            if i >= modulo:
                i = 0
                I += 1
            if I >= modulo:
                I = 0
            lastRunTime = thisRunTime
            checked = []
            clusters = []
            totalClusterCount = 0
            greenPixelCount = 0
        elif currentState == States.Endzone:
            if routeIndex == -2: #Setup
                routeIndex = len(routeList) - 1
            if routeIndex > -1: #Go through the route in reverse order, going in the opposite directions
                actGPIO = oppositeGPIO(routeList[routeIndex][0])
                actTime = routeList[routeIndex][1]
                print('Going ' + nameGPIO(actGPIO) + ' for ' + str(actTime) + ' seconds.')
                gpio.output(actGPIO, 1)
                time.sleep(actTime)
                gpio.output(actGPIO, 0)
                routeIndex -= 1
            else: #Afterwards
                gpio.output(leftGPIO, 1)
                time.sleep(fullTurnTime * (90 / 360))
                gpio.output(leftGPIO, 0)
                moveUntil(backwardGPIO, 'back', 2.5, True)
                moveUntil(forwardGPIO, 'back', 5.5, False)
                gpio.output(rightGPIO, 1)
                time.sleep(fullTurnTime * (90 / 360))
                gpio.output(rightGPIO, 0)
                hugUntil(backwardGPIO, 'back', 'right', 4, 6.5, True, 0.2)
                moveUntil(backwardGPIO, 'back', 2.5, True)
                moveUntil(forwardGPIO, 'back', 16.45, False)
                print('Dropping off the football.')
                gpio.output(pickupGPIO, 1)
                time.sleep(0.00001)
                gpio.output(pickupGPIO, 0)
                retrieveCount += 1
                if retrieveCount < 6:
                    changeState(States.Start)
                else:
                    changeState(States.EndCap)
        elif currentState == States.EndCap:
            pass
