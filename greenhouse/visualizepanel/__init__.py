import pyrebase
from configFiles.config import config

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

crop_data = database.child('CropDevices').get()
crop_device_data = {}

for green_house in crop_data.each():
    for device, crop in green_house.val().items():
        crop_device_data[device] = [crop, green_house.key()]
        
threhoulds = database.child('Threshoulds').get()
crop_min_max = threhoulds.val()



def stream_handler(message):

    # green_house_id = message['path'].split('/')[1]
    if(message['data'] != None):
        if "Humidity" in message["data"]:
            if message['data']['Humidity'] > crop_min_max[ crop_device_data[message["data"]["DeviceId"]][0] ]['max']['Humidity']:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("AC").set(1)
            else:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("AC").set(0)
            
            if message['data']['Humidity'] < crop_min_max[ crop_device_data[message["data"]["DeviceId"]][0] ]['min']['Humidity']:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Humidifier").set(1)
            else:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Humidifier").set(0)

        if "Temperature" in message["data"]:
            if message['data']['Temperature'] > crop_min_max[ crop_device_data[message["data"]["DeviceId"]][0] ]['max']['Temperature']:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Fan").set(1)
            else:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Fan").set(0)

            if message['data']['Temperature'] < crop_min_max[ crop_device_data[message["data"]["DeviceId"]][0] ]['min']['Temperature']:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Heater").set(1)
            else:
                database.child("Controller").child(crop_device_data[message["data"]["DeviceId"]][1]).child("Heater").set(0)


mystream = database.child("Sensor").stream(stream_handler)

