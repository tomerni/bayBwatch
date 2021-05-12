from send_and_recive import send_picture, get_string
import re
#from picamera import PiCamera
from time import sleep
import os
#camera = PiCamera()
from yoloface import _main
from shapely.geometry import Point, Polygon

pool_poly = None
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
    # sorted hot_zone_ coords will look like [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
    # create a polygon out of the coords
    poly_coords = [(hz[0], hz[1]), (hz[2], hz[3]), (hz[4], hz[5]), (hz[6], hz[7])]
    pool_poly = Polygon(poly_coords)


def check_borders(child_coords):

    # create a point out of the coords
    child_x = child_coords[0]
    child_y = 720 - child_coords[1] # 720 is the height of a RPi camera image
    child_point = Point(24.952242, 60.1696017)
    return child_point.within(pool_poly)


def sort_hot_zone_coords(hot_zone_coords):
    # TODO: Write sorting function
    return hot_zone_coords


if __name__ == '__main__':
    main()
