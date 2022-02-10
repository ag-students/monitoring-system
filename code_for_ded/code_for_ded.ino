#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <TimeLib.h>
#include <WiFiUdp.h>

const char* ssid = "LAPTOP-ASUS";
const char* password = "0411PlaTon";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ru.pool.ntp.org", 10800);

char JSON[] = "{\"id\": 0, \"date\": \"00/00/2000\", \"time\": \"00:00:00\", \"move\": _}";

byte last_second, second_, minute_, hour_, day_, month_;
int year_;

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
}

void loop() {
    pinMode(2, INPUT);
    timeClient.update();
    unsigned long unix_epoch = timeClient.getEpochTime();
    second_ = second(unix_epoch);
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    // id of room
        JSON[7] = '2';
        if (last_second != second_) {
            minute_ = minute(unix_epoch);
            hour_   = hour(unix_epoch);
            day_    = day(unix_epoch);
            month_  = month(unix_epoch);
            year_   = year(unix_epoch);
    
            JSON[48] = second_ % 10 + 48;
            JSON[47] = second_ / 10 + 48;
            JSON[45]  = minute_ % 10 + 48;
            JSON[44]  = minute_ / 10 + 48;
            JSON[42]  = hour_   % 10 + 48;
            JSON[41]  = hour_   / 10 + 48;
        
            JSON[19]  = day_   / 10 + 48;
            JSON[20]  = day_   % 10 + 48;
            JSON[22]  = month_  / 10 + 48;
            JSON[23]  = month_  % 10 + 48;
            JSON[27] = (year_   / 10) % 10 + 48;
            JSON[28] = year_   % 10 % 10 + 48;
        }
        last_second = second_;
        if (digitalRead(2) == HIGH) {
          JSON[60] = '1';
        } else {
          JSON[60] = '0';
        }
        Serial.println(JSON);
    
        WiFiClient client;
        HTTPClient http;
        http.begin(client, "http://192.168.137.168:5000/post_json");
        http.addHeader("Content-Type", "application/json");
    
        int httpCode = http.POST(JSON);
        String payload = http.getString();
    
        Serial.println(httpCode);
        Serial.println(payload);
    
        http.end();  //Close connection

    } else {
        Serial.println("Error in WiFi connection");
    }
    delay(20000);  //Send a request every 20 seconds
}
