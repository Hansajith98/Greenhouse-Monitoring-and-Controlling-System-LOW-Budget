import json
import time
import websocket
import pyrebase
from configFiles.config import config

ws = websocket.WebSocket()

ws.connect('ws://127.0.0.1:8000/ws/some_url')

# for i in range(10):
#     time.sleep(2)
#     ws.send(json.dumps({'temperature':50}))



firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def stream_handler(message):
    updated_values['date'] = message['path'].split('/')[1]
    try:
        updated_values['Humidity'] = message['data']["Humidity"]
        updated_values['Temperature'] = message['data']["Temperature"]
        print(updated_values)
        ws.send(json.dumps( updated_values ))
    except:
        pass




if __name__ == '__main__':
    safe_temperature = 20
    safe_humidity = 40

    updated_values = {}
    
    mystream = database.child("Sensor").stream(stream_handler)
