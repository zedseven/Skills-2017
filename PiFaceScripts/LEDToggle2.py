from time import sleep
import pifacedigitalio as p


DELAY = 1.0  # seconds


if __name__ == "__main__":
    p.init()
    pifacedigital = p.PiFaceDigital()
    while True:
        for i in range (8):
            p.digital_write(i,1)
            sleep(DELAY)
            p.digital_write(i,0)
