import json
from sqlite3 import threadsafety
import pyrebase
import pandas as pd
from configFiles.config import config

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

threshoulders = pd.read_csv('min max threshoulders.csv')


for _, row in threshoulders.iterrows():

    payload = {
        "N" : row['N'],
        "P" : row['P'],
        "K" : row['K'],
        "Temperature" : row['temperature'],
        "Humidity" : row['humidity'],
        "Rainfall" : row['rainfall'],
        "PH" : row['ph'],
    } 
    database.child('Threshoulds').child(row['label']).child(row['type']).set(payload)

print(" Firebase Updated! ")



