import pyrebase

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
storage.child("pool_images/pool_image.jpg").put("pool_image.jpg")


database = firebase.database()
info = database.child("info")

info.set({"info": "1,0,0,0.5,1,0.35,1,0.2"})
info.set({"info": "8,8,5,7.5,4,5.8,8,8"})
info.set({"info": "1,0,0,0.5,1,0.35,1,0.2"})


if info.get().each():
    for x in info.get().each():
        print("\n key is: ")
        print(x.key())
        print("\n val is:")
        print(x.val())

