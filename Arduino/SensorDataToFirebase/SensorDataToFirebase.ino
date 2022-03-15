#include <FirebaseESP8266.h>
#include <time.h>

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#include "config.h"

#define LED_PIN 2

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

static int temperature = random(0, 30);
static int humidity = random(10, 80);

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

  //Or use legacy authenticate method
  //config.database_url = DATABASE_URL;
  //config.signer.tokens.legacy_token = "<database secret>";

  //To connect without auth in Test Mode, see Authentications/TestMode/TestMode.ino

  //////////////////////////////////////////////////////////////////////////////////////////////
  //Please make sure the device free Heap is not lower than 80 k for ESP32 and 10 k for ESP8266,
  //otherwise the SSL connection will fail.
  //////////////////////////////////////////////////////////////////////////////////////////////

  Firebase.begin(&config, &auth);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
  Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);

  /** Timeout options.

    //WiFi reconnect timeout (interval) in ms (10 sec - 5 min) when WiFi disconnected.
    config.timeout.wifiReconnect = 10 * 1000;

    //Socket connection and SSL handshake timeout in ms (1 sec - 1 min).
    config.timeout.socketConnection = 10 * 1000;

    //Server response read timeout in ms (1 sec - 1 min).
    config.timeout.serverResponse = 10 * 1000;

    //RTDB Stream keep-alive timeout in ms (20 sec - 2 min) when no server's keep-alive event data received.
    config.timeout.rtdbKeepAlive = 45 * 1000;

    //RTDB Stream reconnect timeout (interval) in ms (1 sec - 1 min) when RTDB Stream closed and want to resume.
    config.timeout.rtdbStreamReconnect = 1 * 1000;

    //RTDB Stream error notification timeout (interval) in ms (3 sec - 30 sec). It determines how often the readStream
    //will return false (error) when it called repeatedly in loop.
    config.timeout.rtdbStreamError = 3 * 1000;

    Note:
    The function that starting the new TCP session i.e. first time server connection or previous session was closed, the function won't exit until the
    time of config.timeout.socketConnection.

    You can also set the TCP data sending retry with
    config.tcp_data_sending_retry = 1;

  */
}

void loop()
{

  if (Firebase.ready() && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();

    time_t now = time(NULL);
    char CurrentTime [80] = "\0";
    strftime(CurrentTime, sizeof(CurrentTime), "%a %b %d %T %Y", localtime(&now));
    String DataRowId = "/Sensor/" + String(CurrentTime) +"/";
    String HumidityId = "Humidity";
    String TemperatureId = "Temperature";
    String DeviceId = "DeviceId";
    humidity = generateSensorValue(humidity);
    temperature = generateSensorValue(temperature);

    digitalWrite(LED_PIN, HIGH);

    FirebaseJson json;
    json.add(HumidityId, humidity);
    json.add(TemperatureId, temperature);
    json.add(DeviceId, "Device01");
    Serial.printf("Update node... %s\n", Firebase.updateNode(fbdo, DataRowId, json) ? "ok" : fbdo.errorReason().c_str());

    Serial.println();
    digitalWrite(LED_PIN, LOW);
  }
}
