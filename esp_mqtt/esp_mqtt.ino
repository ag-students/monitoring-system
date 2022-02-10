#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include <WiFiUdp.h>

const char *ssid            = "TP-Link_AF84";
const char *password        = "20000411lav";

const char *mqtt_broker     = "broker.emqx.io";
const char *topic           = "my_unic_topic_16.32";
const char *mqtt_username   = "esp8266";
const char *mqtt_password   = "20000411lav";
const int   mqtt_port       = 1883;

char        Time[]          = "00:00:00";
char        Date[]          = "00/00/2000";
int         year_;
int         id_room;
byte        last_second, second_, minute_, hour_, day_, month_;

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
    // char *client_id = "esp8266-client-";
    // strcat(client_id, (WiFi.macAddress()).c_str());
    // Serial.println(client_id);
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
    while (!client.connected()) {
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Public emqx mqtt broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.println(client.state());
            delay(2000);
        }
    }
    client.publish(topic, "hello emqx");
    client.subscribe("esp/setup");
}

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
    serializeJsonPretty(doc, JSONmessageBuffer, sizeof(JSONmessageBuffer));

    Serial.println(JSONmessageBuffer);
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    pinMode(2, INPUT);

    timeClient.update();
    unsigned long unix_epoch = timeClient.getEpochTime();
    second_ = second(unix_epoch);  

    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
        // Generate JSON
        StaticJsonDocument<500> doc;
        // id of room
        // IF на ожидание получения id
        if (id_room != 0) {
            doc["id"] = id_room;
            if (last_second != second_) {
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
            }
            last_second = second_;
            doc["date"] = Date;
            doc["time"] = Time;

            if (digitalRead(2) == HIGH){
                doc["move"] = 1;
            } else {
                doc["move"] = 0;
            }
            char JSONmessageBuffer[300];
            serializeJsonPretty(doc, JSONmessageBuffer, sizeof(JSONmessageBuffer));
            Serial.println(JSONmessageBuffer);

            // client.publish(topic, JSONmessageBuffer);
        }
    } else {
        Serial.println("Error in WiFi connection");
    }
    // delay(5000);  //Send a request every 20 seconds
    client.loop();
}
