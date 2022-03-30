#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#include "config.h"

#define FAN 2
#define AC 3
#define HEATER 4
#define HUMIDIFIER 5

//Define Firebase Data object
FirebaseData stream;
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

String greenhouse_id = "greenhouse1";   // Change greenhouseid according to device rregisterd id

unsigned long sendDataPrevMillis = 0;

int count = 0;

volatile bool dataChanged = false;

void streamCallback(StreamData data)
{
  Serial.printf("sream path, %s\nevent path, %s\ndata type, %s\nevent type, %s\n\n",
                data.streamPath().c_str(),
                data.dataPath().c_str(),
                data.dataType().c_str(),
                data.eventType().c_str());
  printResult(data); //see addons/RTDBHelper.h

  int ControllerValue;
  int ControllerPin;

  if (data.dataTypeEnum() == fb_esp_rtdb_data_type_integer)
    ControllerValue = data.to<int>();

  if (data.dataPath() == "/AC") {
    ControllerPin = AC;
    if (ControllerValue == 1) {
      digitalWrite(ControllerPin, LOW);
      Serial.println("AC turend ON");
    } else {
      digitalWrite(ControllerPin, HIGH);
      Serial.println("AC turend OFF");
    }
  }
  if (data.dataPath() == "/Fan") {
    ControllerPin = FAN;
    if (ControllerValue == 1) {
      digitalWrite(ControllerPin, LOW);
      Serial.println("FAN turend ON");
    } else {
      digitalWrite(ControllerPin, HIGH);
      Serial.println("FAN turend OFF");
    }
  }
  if (data.dataPath() == "/Humidifier") {
    ControllerPin = HUMIDIFIER;
    if (ControllerValue == 1) {
      digitalWrite(ControllerPin, LOW);
      Serial.println("HUMIDIFIER turend ON");
    } else {
      digitalWrite(ControllerPin, HIGH);
      Serial.println("HUMIDIFIER turend OFF");
    }
  }
  if (data.dataPath() == "/Heater") {
    ControllerPin = HEATER;
    if (ControllerValue == 1) {
      digitalWrite(ControllerPin, LOW);
      Serial.println("HEATER turend ON");
    } else {
      digitalWrite(ControllerPin, HIGH);
      Serial.println("HEATER turend OFF");
    }
  }



  //This is the size of stream payload received (current and max value)
  //Max payload size is the payload size under the stream path since the stream connected
  //and read once and will not update until stream reconnection takes place.
  //This max value will be zero as no payload received in case of ESP8266 which
  //BearSSL reserved Rx buffer size is less than the actual stream payload.
  Serial.printf("Received stream payload size: %d (Max. %d)\n\n", data.payloadLength(), data.maxPayloadLength());

  //Due to limited of stack memory, do not perform any task that used large memory here especially starting connect to server.
  //Just set this flag and check it status later.
  dataChanged = true;
}

void streamTimeoutCallback(bool timeout)
{
  if (timeout)
    Serial.println("stream timed out, resuming...\n");

  if (!stream.httpConnected())
    Serial.printf("error code: %d, reason: %s\n\n", stream.httpCode(), stream.errorReason().c_str());
}

void setup()
{
  pinMode(FAN, OUTPUT);
  pinMode(AC, OUTPUT);
  pinMode(HUMIDIFIER, OUTPUT);
  pinMode(HEATER, OUTPUT);

  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the user sign in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  //Or use legacy authenticate method
  //config.database_url = DATABASE_URL;
  //config.signer.tokens.legacy_token = "<database secret>";

  //To connect without auth in Test Mode, see Authentications/TestMode/TestMode.ino

  Firebase.begin(&config, &auth);

  Firebase.reconnectWiFi(true);

  //Recommend for ESP8266 stream, adjust the buffer size to match your stream data size
#if defined(ESP8266)
  stream.setBSSLBufferSize(2048 /* Rx in bytes, 512 - 16384 */, 512 /* Tx in bytes, 512 - 16384 */);
#endif
  String datapath = "/Controller/" + greenhouse_id;
  if (!Firebase.beginStream(stream, datapath))
    Serial.printf("sream begin error, %s\n\n", stream.errorReason().c_str());

  Firebase.setStreamCallback(stream, streamCallback, streamTimeoutCallback);

}

void loop()
{
  if (dataChanged)
  {
    dataChanged = false;
    Serial.printf("Recieved...");
  }
}
