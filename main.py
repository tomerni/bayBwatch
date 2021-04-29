# if first usage:
    # send photo
    # while no answer:
        # wait
    #turn string into tuples of coordinates
    #open text file in RPi
    #save coordinates into text file

# send to main
from send_and_recive import send_string, get_string

from picamera import PiCamera
from time import sleep

camera = PiCamera()
from yoloface import _main


def main(is_first_usage):
    if is_first_usage:
        take_picture()
        send_string("pool_image.jpg")
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
