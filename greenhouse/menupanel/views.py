from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pyrebase

from configFiles.config import config
from greenhouse.decorators import login_necessary

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

greenhouse_data_from_fire = database.child('CropDevices').get()
greenhouse_names = []
for green_house in greenhouse_data_from_fire.each():
    greenhouse_names.append(green_house.key())

@login_necessary()
def menupanel(request):
    context = {'greenhouse_names':greenhouse_names}
    return render(request, 'menupanel.html', context=context)




