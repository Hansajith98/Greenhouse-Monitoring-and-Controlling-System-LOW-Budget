from django.shortcuts import render, redirect, reverse
import pyrebase
from django.contrib.auth import login

from configFiles.config import config


firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, "Login.html")


def home(request):
    return render(request, "menupanel.html")


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "Login.html", {"message": message})
    session_id = user['idToken']
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
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email, passs)
        authe.send_email_verification(user['idToken'])
        print(authe.get_account_info(user['idToken']))
    except:
        print("cant")
        return render(request, "Registration.html")
    return redirect(reverse('login'))
