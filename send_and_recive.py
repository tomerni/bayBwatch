import requests
import json

def send_string(string):
    url = "https://pools-guard.herokuapp.com"
    Data = requests.post(url, json =
    json.loads('{"user":"salay", "password":"salay123", "data":' + '"' +string + '"' + '}'))
    return Data.content

def send_file(file_path):
    with open(file_path, "rb") as a_file:
        myfiles = {'file': a_file}
        url = "https://pools-guard.herokuapp.com"
        Data = requests.post(url,files = myfiles,  json =
        json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content

def get_string():
    url = "https://pools-guard.herokuapp.com"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content.decode()

def get_file():
    url = "https://pools-guard.herokuapp.com"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content

