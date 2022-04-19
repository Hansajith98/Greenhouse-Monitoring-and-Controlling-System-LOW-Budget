import json
import time
import websocket
import pyrebase
from configFiles.config import config

ws = websocket.WebSocket()

ws.connect('ws://127.0.0.1:8000/ws/dashboard')


firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def stream_handler(message):
    if(message['data'] != None):
        if "Humidity" in message["data"]:
            updated_values['greenhouse_id'] = message['path'].split('/')[1]
            updated_values['date'] = message['path'].split('/')[2]
            try:
                updated_values['Humidity'] = message['data']["Humidity"]
                updated_values['Temperature'] = message['data']["Temperature"]

                ws.send(json.dumps( updated_values ))
            except:
                pass




if __name__ == '__main__':

    updated_values = {}
    
    mystream = database.child("Sensor").stream(stream_handler)
