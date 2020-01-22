import pygame
from pygame.locals import *
import picamera
import picamera.array

res = (128, 64)

pygame.init()
pygame.display.set_caption('MiniFootball Detection Feed', 'Cam Feed')
screen = pygame.display.set_mode((res[0] * 8, res[1] * 8))
pygame.draw.rect(screen, (100, 100, 100), (0, 0, 4, 4), 0)

with picamera.PiCamera() as camera:
    #picamera.readthedocs.io/en/release-1.10/api_camera.html
    camera.framerate = 30
    camera.resolution = res
    camera.exposure_mode = 'sports' #off, auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    camera.exposure_compensation = 25
    camera.awb_mode = 'flash' #off, auto, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon
    camera.vflip = 1
    camera.hflip = 1
    drawToScreenPs = 8

    while True:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='rgb')#'bgr')
            image = stream.array
            for y in range(len(image)):
                for x in range(len(image[y])):
                    r = image[y][x][0]
                    g = image[y][x][1]
                    b = image[y][x][2]
                    pygame.draw.rect(screen, (r, g, b), (x * drawToScreenPs, y * drawToScreenPs, drawToScreenPs, drawToScreenPs), 0)
            pygame.display.update()
