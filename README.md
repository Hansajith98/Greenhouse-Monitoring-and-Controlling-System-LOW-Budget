# Greenhouse-Monitoring-and-Controlling-System-LOW-Budget
This repository belongs to a system that control and monitor greenhouse automatically in Low Budget way. This is combination of arduino and django as main technologies.

### The main purpose of this system is monitor and automatically control the greenhouse in a low budget with allowing ultimate flexibility.

## Plants which users can use with system 
- apple
- banana
- blackgram
- chickpea
- coconut
- coffee
- cotton
- grapes
- jute
- kidneybeans
- lentil
- maize
- mango
- mothbeans
- mungbean
- muskmelon
- orange
- papaya
- pigeonpeas
- pomegranate
- rice
- watermelon

### Structure of system
![Systemm Structure](https://i.postimg.cc/j2ZMZDQZ/Untitled-document.jpg)

### File Structure
- Arduino
  - FirebaseToController - Get controling data from firebase when database updated, and control greenhouse. 
  - SensorDataToFirebase - Send sensor data to the firebase within every 90 seconds.
- greeenhouse - Django application for User dashboard and also it will set controller on and off based on sensor data. This also create and run websocket to send data to the front-end.
- Websocket Client - Serverside script for sending real-time updating data to the front-end when firebase data changed.

##### How to run the project
1. Clone the repository.
2. Create `config.h` file in `FirebaseToController` and `SensorDataToFirebase`.
Structure of `config.h` file
<pre>
    /* 1. Define the WiFi credentials */
    #define WIFI_SSID "Your wifi SSD"
    #define WIFI_PASSWORD "Your WiFi Password"

    /* Leave this line without editing */
    #define NTP_SERVERS "pool.ntp.org", "time.nist.gov"

    //For the following credentials, see examples/Authentications/SignInAsUser/EmailPassword/EmailPassword.ino

    /* 2. Define the API Key */
    #define API_KEY "Firebase_Web_API_Key"

    /* 3. Define the RTDB URL */
    #define DATABASE_URL "https://<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabaseapp/"

    /* 4. Define the user Email and password that alreadey registerd or added in your project */
    #define USER_EMAIL "example@mail.com"
    #define USER_PASSWORD "Password"
</pre>
3. Create config.py within directory `greenhouse/ConfigFiles/`. It's structure will as follow,
<pre>
    # Remember the code we copied from Firebase.
    # This can be copied by clicking on the settings icon > project settings, then scroll down in your firebase dashboard

    config = {
        "apiKey": "Firebase_Web_API_Key",
        "authDomain": "<projectId>.firebaseapp.com",
        "databaseURL": "https://<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabaseapp/",
        "projectId": "greenhousefire-63b38",
        "storageBucket": "<projectId>.appspot.com",
        "messagingSenderId": "Message_Sending_ID",
        "appId": "App_ID",
        "measurementId": "Measurement_ID"
    }
</pre>
4. Run Redis Server.
5. Run dajngo `python greenhouse/manage.py runserver`.
6. Run `python client.py` to run script to write data on Web Socket.
7. Upload `FirebaseToController`, `SensorDataToFirrebase` files to the ESP8266 Controlling module and Sensor Hub module.
8. Browse for `http://127.0.0.1:8000/` to get User-Dashboard.

