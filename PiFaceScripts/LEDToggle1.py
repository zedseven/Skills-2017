from time import sleep
import pifacedigitalio


DELAY = 1.0  # seconds


if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()
    while True:
        for i in range (8):
            pifacedigital.leds[i].toggle()
        sleep(DELAY)
