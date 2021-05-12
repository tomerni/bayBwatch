from picamera import PiCamera
from time import sleep
import os
#camera = PiCamera()
from yoloface import _main
from shapely.geometry import Point, Polygon
import pyrebase


global pool_poly
pool_poly = [None]
PASSWORD = "1234"

config = {
    "apiKey": "AIzaSyDNGQpnIZk5-h5-zaz8zrUKfVg77xBjlTg",
    "authDomain": "life-guard-da054.firebaseapp.com",
    "databaseURL": "https://life-guard-da054-default-rtdb.firebaseio.com",
    "projectId": "life-guard-da054",
    "storageBucket": "life-guard-da054.appspot.com",
    "messagingSenderId": "286029846592",
    "appId": "1:286029846592:web:fd6397ad9d2030d00ea7a5",
    "measurementId": "G-4EFRYT3YQQ"
};

# save image to db
# retrieve string
firebase = pyrebase.initialize_app(config)

database = firebase.database()
borders = database.child("borders")

storage = firebase.storage()
#images = storage.child("images")


def main():
    if not os.path.exists("coords"):
        # wait for a password
        password = borders.get().val()
        while password != PASSWORD:
            password = borders.get().val()
        communication()
    _main()


def communication():
    take_picture()
    storage.child("images/pool_image.jpg")
    while "," not in borders.get().val():
        # TODO: Check the format borders are returned from db
        take_picture()
        storage.child("images/pool_image.jpg") # TODO: Check if there's overloading
    string_to_poly(borders.get().val())


def take_picture():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/bayBwatch/pool_image.jpg')
    camera.stop_preview()


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
