#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include <WiFiUdp.h>

// Global for Wi-Fi & MQTT
const String  client_id              = "esp8266-client-" + WiFi.macAddress();
const char   *ssid           PROGMEM = "TP-Link_AF84";
const char   *password       PROGMEM = "20000411lav";
const char   *mqtt_broker    PROGMEM = "broker.emqx.io";
const char   *topic          PROGMEM = "ololo/pir_data";
const char   *mqtt_username  PROGMEM = "esp8266";
const char   *mqtt_password  PROGMEM = "20000411lav";
const int     mqtt_port      PROGMEM = 1883;

// Global for Time
      char    Time[]                 = "00:00:00";
      char    Date[]                 = "00/00/2000";
      int     time_delay             = 2000; // Timer
      int     year_;
      int     id_room;
      byte    last_second, second_, minute_, hour_, day_, month_;

WiFiClient      espClient;
PubSubClient    client(espClient);
WiFiUDP         ntpUDP;
NTPClient       timeClient(ntpUDP, "ru.pool.ntp.org", 10800);

void setup() {
    Serial.begin(115200);
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    Serial.println();

    Serial.println(client_id);
    while (!client.connected()) {
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Broker connected");
        } else {
            Serial.print("faile: ");
            Serial.println(client.state());
            delay(2000);
        }
    }
    client.publish(topic, "hello emqx");
    client.subscribe("esp/setup");
}

// Callback for new ID
void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.println("Message:");

    StaticJsonDocument <256> doc;
    deserializeJson(doc, payload);

    if (WiFi.macAddress().c_str() == doc["mac"]) {
        id_room = doc["id"];
    }
    char JSONmessageBuffer[256];
    serializeJsonPretty(doc, JSONmessageBuffer, 256);

    Serial.println(JSONmessageBuffer);
    Serial.println();
    Serial.println("-----------------------");
    time_delay = 0;
}

// Send message in topic ololo/pir_data
void send_message() {
    StaticJsonDocument<500> doc;
    unsigned long unix_epoch = timeClient.getEpochTime();
    
    if (id_room != 0 && time_delay == 0) {
        second_  = second(unix_epoch);
        minute_  = minute(unix_epoch);
        hour_    = hour(unix_epoch);
        day_     = day(unix_epoch);
        month_   = month(unix_epoch);
        year_    = year(unix_epoch);

        Time[7]  = second_ % 10 + 48;
        Time[6]  = second_ / 10 + 48;
        Time[4]  = minute_ % 10 + 48;
        Time[3]  = minute_ / 10 + 48;
        Time[1]  = hour_   % 10 + 48;
        Time[0]  = hour_   / 10 + 48;

        Date[0]  = day_    / 10 + 48;
        Date[1]  = day_    % 10 + 48;
        Date[3]  = month_  / 10 + 48;
        Date[4]  = month_  % 10 + 48;
        Date[8]  = (year_  / 10) % 10 + 48;
        Date[9]  = year_   % 10 % 10 + 48;

        doc["id"] = id_room;
        doc["date"] = Date;
        doc["time"] = Time;

        if (digitalRead(2) == HIGH) {
            doc["move"] = 1;
        } else {
            doc["move"] = 0;
        }
        char JSONmessageBuffer[300];
        serializeJsonPretty(doc, JSONmessageBuffer, 300);
        Serial.println(JSONmessageBuffer);

        client.publish(topic, JSONmessageBuffer);
        time_delay = 2000;
    }
    time_delay --;
    delay(10);
}

void loop() {
    pinMode(2, INPUT);
    // Update time & date
    while(!timeClient.update()) {
        timeClient.forceUpdate();
    }
    if (WiFi.status() == WL_CONNECTED) {
        send_message();
    } else {
        Serial.println("Error in WiFi connection");
    }
    client.loop();
}
