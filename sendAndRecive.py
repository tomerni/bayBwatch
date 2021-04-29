import requests
import json
def send_string(string):
    url = "https://pools-guard.herokuapp.com"
    Data = requests.post(url, json =
    json.loads('{"user":"salay", "password":"salay123", "data":' + '"' +string + '"' + '}'))
    return Data.content

def get_string():
    url = "https://pools-guard.herokuapp.com"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content
