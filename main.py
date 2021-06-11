from picamera import PiCamera
from time import sleep
import os
from yoloface import _main
import pyrebase

PASSWORD = "1234"
camera = PiCamera()

# Or needs to set any data to the child "info".
# that is, for passowrd: "info":"1234", for borders: "info":"0,0,1,1,0,0,1,1"

def main():
    pool_coords = []
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

    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()
    # images = storage.child("images")


    database = firebase.database()
    info = database.child("info")

    if not os.path.exists("coords"):
        # wait for a password
        while not info.get().each():
            continue
        print("Looking for coords")
        password = ""
        for x in info.get().each():
            password = x.val()
            print(password)
        while password != PASSWORD:
            print("Wrong password, waiting to get the right one")
            # Maybe send somehow a message that the password is wrong
            for x in info.get().each():
                password = x.val()
        print("Password is correct")
        process_pool_img(storage, info)
    pool_coords = retrieve_coords()
    info.remove()
    camera.close()
    _main() #info, pool_coords


def process_pool_img(storage, info):
    take_picture()
    storage.child("images/pool_image.jpg").put("pool_image.jpg")
    print("Image is uploaded to storage")
    response = ""
    for x in info.get().each():
        response = x.val()
        print("first try: " + response)
    # TODO: If the user wants another picture, response is "1234 N"
    while "," not in response:
        if "N" in response:
            take_picture()
            storage.child("images/pool_image.jpg")  # TODO: Check if there's overloading
        for x in info.get().each():
            response = x.val()
    print("final try: " + response)
    borders = ""
    for x in info.get().each():
        borders = x.val()
    string_to_poly(borders) # TODO: Same as above


def take_picture():
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/bayBwatch/pool_image.jpg')
    camera.stop_preview()
    print("took picture")


def string_to_poly(coords_string):# "0.11, 0.33, 0.6456, 0.555, 1, 0.222, 0,7, 0"
    f = open("coords", "w")
    for coord in coords_string.split(","):
        f.write(coord + "\n")
    f.close()


def retrieve_coords():
    f = open("coords", "r")
    lines = f.readlines()
    hz = []
    for line in lines:
        hz.append(line[:-1]) # TODO: Check if removing \n is really needed
    i = 0
    hz_tuples =[]
    while(i < 7):
        hz_tuples.append((hz[i], hz[i+1]))
        i += 2
    return hz_tuples


if __name__ == '__main__':
    main()
