from django.shortcuts import render, redirect, reverse
import pyrebase
from django.contrib.auth import login

from configFiles.config import config
from greenhouse.decorators import login_necessary

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, "Login.html")

@login_necessary()
def home(request):
    return render(request, "menupanel.html")


def postsignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        print(message)
        return render(request, "Login.html", {"message": message})
    session_id = user['localId']
    print(session_id)
    request.session['uid'] = str(session_id)

    return redirect(reverse('menupanel'))


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "Login.html")


def signUp(request):
    return render(request, "Registration.html")


def postsignUp(request):
    username = request.POST.get('user_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.create_user_with_email_and_password(email, password)
        authe.send_email_verification(user['idToken'])
        database.child("User_Info").child(user['localId']).set({'User_Name':username})
    except:
        print("cant create")
        message = "Please ChecK your Data"
        return render(request, "Registration.html", {"message": message})
    
    return redirect(reverse('login'))
