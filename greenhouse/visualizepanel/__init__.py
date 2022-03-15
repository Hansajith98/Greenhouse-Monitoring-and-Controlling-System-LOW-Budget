import pyrebase
from configFiles.config import config

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

safe_temperature = 50
safe_humidity = 20



def stream_handler(message):
    if "Humidity" in message["data"]:
        if message['data']['Humidity'] > safe_humidity:
            database.child("Controller").child("Light").set(1)
        else:
            database.child("Controller").child("Light").set(0)

    if "Temperature" in message["data"]:
        if message['data']['Temperature'] > safe_humidity:
            database.child("Controller").child("Fan").set(1)
        else:
            database.child("Controller").child("Fan").set(0)


mystream = database.child("Sensor").stream(stream_handler)
