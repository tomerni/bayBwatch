# send to main
from send_and_recive import send_picture, get_string

from picamera import PiCamera
from time import sleep
import os
camera = PiCamera()
from yoloface import _main


def main():
    if not os.path.exists("coords"):
        take_picture()
        send_picture("pool_image.jpg", 1,1)
        while not get_string():
            continue
        string_to_coords(get_string())
        _main()


def take_picture():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/bayBwatch/pool_image.jpg')
    camera.stop_preview()


def string_to_coords(coords_string):
    f = open("coords", "w")
    for coord in coords_string:
        f.write(coord + "\n")
