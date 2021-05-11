# send to main
from send_and_recive import send_picture, get_string

#from picamera import PiCamera
from time import sleep
import os
#camera = PiCamera()
from yoloface import _main


def main():
    if not os.path.exists("coords"):
        # wait for a password
        password = get_string()
        while password != "1234":
            password = get_string()
        # when password is correct, take and send the picture
        take_picture()
        send_picture("pool_image.jpg", "salay", "salay123")
        while not get_string():
            continue
        string_to_coords(get_string())
        _main()


def take_picture():
    #camera.start_preview()
    sleep(2)
    #camera.capture('/home/pi/bayBwatch/pool_image.jpg')
    #camera.stop_preview()


def string_to_coords(coords_string):
    f = open("coords", "w")
    for coord in coords_string:
        f.write(coord + "\n")


def check_borders(real_coords):
    # function assumes the following order:
    # right
    f = open("coords", "r")
    lines = f.readlines()
    hot_zone_coords = []
    for line in lines:
        hot_zone_coords.append(line)
    if hot_zone_coords[0] >= real_coords[0] and hot_zone_coords[1] >= real_coords[1] and hot_zone_coords[2] >= real_coords[2] and hot_zone_coords[3] >= real_coords[3]:
        return True
    else:
        return False
