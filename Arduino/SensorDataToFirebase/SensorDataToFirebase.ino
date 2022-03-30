#include <FirebaseESP8266.h>
#include <time.h>

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#include "config.h"

#define LED_PIN 2

String greenhouse_id = "greenhouse1";   // Change this with greenhouse id the device is assigned
String device_id = "Device01";    // Change this with device id

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

static int temperature = random(0, 30);
static int humidity = random(10, 100);

unsigned long sendDataPrevMillis = 0;


static void initializeTime()
{
  Serial.print("Setting time using SNTP");

  configTime(5.5 * 3600, 0, NTP_SERVERS);
  time_t now = time(NULL);
  while (now < 1510592825)
  {
    delay(500);
    Serial.print(".");
    now = time(NULL);
  }
  Serial.println("done!");
}

static char* getCurrentLocalTimeString()
{
  time_t now = time(NULL);
  return ctime(&now);
}

static void printCurrentTime()
{
  Serial.print("Current time: ");
  Serial.print(getCurrentLocalTimeString());
}

static int generateSensorValue( int recentValue )
{
  if (recentValue - 5 < 0) {
    return (int)random(recentValue, recentValue + 10);
  } else if (recentValue + 5 > 100) {
    return (int)random(recentValue - 10, recentValue);
  } else {
    return (int)random(recentValue - 5, recentValue + 5);
  }
}

void setup()
{
  pinMode(LED_PIN, OUTPUT);

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

  initializeTime();
  printCurrentTime();

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

  Firebase.begin(&config, &auth);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
  Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);

}

void loop()
{

  if (Firebase.ready() && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();

    time_t now = time(NULL);
    char CurrentTime [80] = "\0";
    strftime(CurrentTime, sizeof(CurrentTime), "%a %b %d %T %Y", localtime(&now));
    String DataRowId = "/Sensor/" + greenhouse_id + "/" + String(CurrentTime) + "/";
    String HumidityId = "Humidity";
    String TemperatureId = "Temperature";
    String DeviceId = "DeviceId";
    humidity = generateSensorValue(humidity);
    temperature = generateSensorValue(temperature);

    digitalWrite(LED_PIN, HIGH);

    FirebaseJson json;
    json.add(HumidityId, humidity);
    json.add(TemperatureId, temperature);
    json.add(DeviceId, device_id);
    Serial.printf("Update node... %s\n", Firebase.updateNode(fbdo, DataRowId, json) ? "ok" : fbdo.errorReason().c_str());

    Serial.println();
    digitalWrite(LED_PIN, LOW);
  }
}
