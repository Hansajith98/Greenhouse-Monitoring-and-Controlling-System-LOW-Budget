from django.shortcuts import render, redirect, reverse
import pyrebase

from configFiles.config import config
from greenhouse.decorators import login_necessary

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()



@login_necessary() 
def menupanel(request):
    user_name = request.session['uname']
    greenhouse_data_from_fire = database.child('CropDevices').get()
    greenhouse_names = []
    greenhouse_id = []
    for green_house in greenhouse_data_from_fire.each():
        greenhouse_names.append(green_house.val()['Name'])
        greenhouse_id.append(green_house.key())
    greenhouse_data = zip(greenhouse_names, greenhouse_id)
    context = {'greenhouse_data':greenhouse_data, 'user_name':user_name}
    return render(request, 'menupanel.html', context=context)


@login_necessary()
def new_greenhouse(request):
    user_name = request.session['uname']
    context = {'user_name':user_name}
    return render(request, 'newgreenhouse.html', context=context)


@login_necessary()
def add_new_greenhouse(request):
    greenhouse_name = request.POST.get('greenhouse_name')
    greenhouse_id = request.POST.get('greenhouse_id')
    device_name = request.POST.get('device_name')
    crop_type = request.POST.get('crop_type')
    new_greenhouse = {device_name:crop_type, 'Name':greenhouse_name}
    try:
        database.child("CropDevices").child(greenhouse_id).set(new_greenhouse)
    except:
        print("cant")
        return render(request, "newgreenhouse.html")
    return redirect(reverse('menupanel'))



