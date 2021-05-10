from urllib.request import urlretrieve

import requests
import json
from PIL import Image


def send_string(string):
    url = "https://pools-guard.herokuapp.com/pictures"
    Data = requests.post(url, json =
    json.loads('{"user":"salay", "password":"salay123", "data":' + '"' +string + '"' + '}'))
    return Data.content


def get_string():
    url = "https://pools-guard.herokuapp.com/pictures"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content
