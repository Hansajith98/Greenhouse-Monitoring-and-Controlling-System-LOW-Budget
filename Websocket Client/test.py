import pyrebase
from configFiles.config import config

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

print(database.child('Threshoulds').get().val())
