import requests
import json


def send_string(string):
    url = "https://pools-guard.herokuapp.com/borders"
    Data = requests.post(url, json =
    json.loads('{"user":"salay", "password":"salay123", "data":' + '"' +string + '"' + '}'))
    return Data.content


def send_picture(file_path, user, password):
    j = '{"user": "%s", "password": "%s"}' % (user, password)
    with open(file_path,'rb') as f:
        files = [
            ('file', (file_path, f, 'application/octet')),
            ('json', ('json', j, 'application/json'))
        ]
        status = requests.post(r'https://pools-guard.herokuapp.com/pictures', files=files)
        print(status.content)


def get_string():
    url = "https://pools-guard.herokuapp.com/borders"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    return Data.content.decode()


def get_file():
    url = "https://pools-guard.herokuapp.com/pictures"
    Data = requests.get(url, json =
    json.loads('{"user":"salay", "password":"salay123"}'))
    file = open("sample_image.png", "wb")
    file.write(Data.content)
    file.close()
    return Data.content

