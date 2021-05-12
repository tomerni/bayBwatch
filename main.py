from send_and_recive import send_picture, get_string
import re
#from picamera import PiCamera
from time import sleep
import os
#camera = PiCamera()
from yoloface import _main
from shapely.geometry import Point, Polygon

global pool_poly
pool_poly = [None]
PASSWORD = "1234"


def main():
    if not os.path.exists("coords"):
        # wait for a password
        password = get_string()
        while password != PASSWORD:
            password = get_string()
        communication()
    _main()


def communication():
    take_picture()
    send_picture("pool_image.jpg", "salay", "salay123")
    while "," not in get_string():
        take_picture()
        send_picture("pool_image.jpg", "salay", "salay123")
    string_to_poly(get_string())


def take_picture():
    #camera.start_preview()
    sleep(2)
    #camera.capture('/home/pi/bayBwatch/pool_image.jpg')
    #camera.stop_preview()


def string_to_poly(coords_string):
    f = open("coords", "w")
    for coord in coords_string:
        f.write(coord + "\n")
    lines = f.readlines()
    hz = []
    for line in lines:
        hz.append(line)
    sort_hot_zone_coords(hz)
    poly_coords = [(hz[0], hz[1]), (hz[2], hz[3]), (hz[4], hz[5]), (hz[6], hz[7])]
    pool_poly[0] = Polygon(poly_coords)


def sort_hot_zone_coords(hot_zone_coords):
    # TODO: Write sorting function
    return hot_zone_coords


def get_pool_poly():
    return pool_poly


if __name__ == '__main__':
    main()
