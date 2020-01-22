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


#Name: Zacchary Dempsey-Plante
#Started: 2016-10-18
#Description: A script that makes use of the Raspberry Pi Camera to look for
#   miniature footballs, find them, identify them, and navigate a robot towards
#   them to pick them up.
#Written for: The 2017 Robotics Club competition.
#Python version: 3.4.2

import pygame, sys, math
from pygame.locals import *
from datetime import datetime
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
gpio.setup(forwardGPIO, gpio.OUT, initial=gpio.LOW)
backwardGPIO = 31
gpio.setup(backwardGPIO, gpio.OUT, initial=gpio.LOW)
leftGPIO = 33
gpio.setup(leftGPIO, gpio.OUT, initial=gpio.LOW)
rightGPIO = 35
gpio.setup(rightGPIO, gpio.OUT, initial=gpio.LOW)
pickupGPIO = 37
gpio.setup(pickupGPIO, gpio.OUT, initial=gpio.LOW)
#gpioPins = [29, 31, 33, 35, 37]
#for p in range(len(gpioPins)):
#    gpio.setup(gpioPins[p], gpio.OUT, initial=gpio.LOW)
#    gpio.output(gpioPins[p], 1)
#    time.sleep(0.5)
#    gpio.output(gpioPins[p], 0)
res = (128, 64)

hasHead = True
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
    compiled = False #for checking to see if the other clusters have already been collpased into it
    absorbedBy = 'none' #cluster that absorbed it - for calcuations
    
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

def calcCID(x, y):
    return '#' + str(x) + '/' + str(y)

def checkPixel(coords):
    global hasHead
    #printv("Analyzing " + str(coords), 2)
    global image
    global checked
    global checkCoords
    global clusters
    global brown
    global brownBuffer
    #printv("Length of checked: " + str(len(checked)), 4)
    if coords.cid + ' : ' + coords.ref + ' : 0' not in checked and coords.cid + ' : ' + coords.ref + ' : 1' not in checked:
        checked.append(coords.cid + ' : ' + coords.ref + ' : 0')
        checkedIndex = len(checked) - 1
        #printv(str(coords) + " has not been checked!", 3)
        cx = coords.x
        cy = coords.y
        
        r = int(image[cy][cx][0])
        g = int(image[cy][cx][1])
        b = int(image[cy][cx][2])
        
        total = r + g + b
        ratio = (r / total, g / total, b / total)
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
            if cx > 0:
                #printv(str((coords.x - 1, coords.y)) + " is being called!", 4)
                checkCoords.append(Coord(cx - 1, cy, coords.cid))
            if cx < res[0] - 1:
                #printv(str((coords.x + 1, coords.y)) + " is being called!", 4)
                checkCoords.append(Coord(cx + 1, cy, coords.cid))
            if cy > 0:
                #printv(str((coords.x, coords.y - 1)) + " is being called!", 4)
                checkCoords.append(Coord(cx, cy - 1, coords.cid))
            if cy < res[1] - 1:
                #printv(str((coords.x, coords.y + 1)) + " is being called!", 4)
                checkCoords.append(Coord(cx, cy + 1, coords.cid))
        else:
            if hasHead == True:
                pygame.draw.ellipse(screen, (0, 255, 0), (cx * drawToScreenPs, cy * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
                pygame.display.update()
    #else:
    #    if hasHead == True:
    #        pygame.draw.ellipse(screen, (255, 0, 0), (coords.x * drawToScreenPs, coords.y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 2)
    #        pygame.display.update()
        
    checkCoords.remove(coords)
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

with picamera.PiCamera() as camera:
    camera.framerate = 30
    camera.resolution = res
    camera.exposure_compensation = 25
    camera.vflip = 1
    cameraFOV = (27.5 * 2) #(15 * 2)#27.5° from the center (straight out) to the edge of the view - really anything from 15-20°. (I didn't have a protractor at the time)
    fullMoveTime = 2 #time taken to move forward fullMoveDistance in seconds
    fullMoveDistance = 30 #distance in cm
    fullTurnTime = 4 #time taken to perform a full 360° turn in seconds
    forwardSensitivity = 4 #how close to the center a football must be before going to pick it up
    pickupSize = 500
    pickupSensitivity = 100 #how close to the ideal football screen size a football should be before pickup
    modulo = 8
    drawToScreenPs = 8
    brownBuffer = 0.05#0.02
    brown = (128, 90, 62)#(143, 111, 107)#(153, 111, 107)#(79, 80, 79)#(81, 55, 34)#(102, 26, 0)#(115, 98, 103)#(84, 61, 42)#(139, 69, 19)
    brownTotal = brown[0] + brown[1] + brown[2]
    brown = (brown[0] / brownTotal, brown[1] / brownTotal, brown[2] / brownTotal)
    #perfectWhite = (133, 133, 133)#(122, 126, 81)#(255, 255, 255)
    #print(camera.contrast)
    #if hasHead == True:
        #print("Please put a white piece of paper 1ft in front of the camera to calibrate the brown-colour search. Press enter when ready.")
        #input()
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
    time.sleep(2)
    lastRunTime = datetime.now()
    thisRunTime = lastRunTime
    deltaTime = None #lastRunTime - thisRunTime
    deltaMillis = None #((deltaTime.days * 24 * 60 * 60 + deltaTime.seconds) * 1000 + deltaTime.microseconds / 1000.0)
    lastTurnDir = 0 #0 for left, 1 for right
    i = 0
    I = 0
    while 1 == 1:
        thisRunTime = datetime.now()
        deltaTime = lastRunTime - thisRunTime
        deltaMillis = ((deltaTime.days * 24 * 60 * 60 + deltaTime.seconds) * 1000 + deltaTime.microseconds / 1000.0)
        
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='rgb')#'bgr')
            image = stream.array
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
                    coords = Coord(x, y, 'none')
                    if x % modulo == i and y % modulo == I:
                        checkCoords.append(coords)
                    #print('(' + str(x) + ', ' + str(y) + ') : (' + str(r) + ', ' + str(g) + ', ' + str(b) + ')')
            while len(checkCoords) > 0:
                checkPixel(checkCoords[0])
            print('Handling clusters.')
            #find/create all clusters
            for c in range(len(checked)):
                split = checked[c].split(' : ') #receives a string in the format of cid : ref : isBrown
                cid = split[0] #format: '#X/Y'
                ref = split[1] #can either be 'none' or another cid
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
                if closestCluster[1] / largestCluster[1] >= 0.65:
                    targetCluster = closestCluster
                else:# if closestCluster[2] / largestCluster[2]:
                    targetCluster = largestCluster
                turnAmnt = (targetCluster[2] / int(res[0] / 2)) * (cameraFOV / 2)
                turnTime = (0 if turnAmnt == 0 else fullTurnTime * (abs(turnAmnt) / 360))
                moveAmnt = abs(1 - (targetCluster[1] / pickupSize))
                moveTime = moveAmnt * fullMoveTime
                if turnAmnt >= forwardSensitivity: #turn right
                    print('Turn ' + str(abs(turnAmnt)) + '° right. (turn right for ' + str(turnTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                    gpio.output(rightGPIO, 1)
                elif turnAmnt <= -forwardSensitivity: #turn left
                    print('Turn ' + str(abs(turnAmnt)) + '° left. (turn left for ' + str(turnTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                    gpio.output(leftGPIO, 1)
                else: #go forward
                    if targetCluster[1] >= (pickupSize + pickupSensitivity):
                        print('Move ' + str(abs(turnAmnt) * fullMoveDistance) + 'cm forwards. (move forwards for ' + str(moveTime) + ' seconds towards cluster ' + str(targetCluster[0]) + ')')
                        gpio.output(forwardGPIO, 1)
                    elif targetCluster[1] <= (pickupSize - pickupSensitivity):
                        print('Move ' + str(abs(turnAmnt) * fullMoveDistance) + 'cm backwards. (move backwards for ' + str(moveTime) + ' seconds away from cluster ' + str(targetCluster[0]) + ')')
                        gpio.output(backwardGPIO, 1)
                    else:
                        print('Pick up the football! (displayed as cluster ' + str(targetCluster[0]) + ')')
                        gpio.output(pickupGPIO, 1)
                time.sleep(turnTime)
                gpio.output(forwardGPIO, 0)
                gpio.output(backwardGPIO, 0)
                gpio.output(leftGPIO, 0)
                gpio.output(rightGPIO, 0)
                gpio.output(pickupGPIO, 0)
            #allow time for viewing results
            if hasHead == True:
                time.sleep(0.5)
            print('Done.')
            
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
