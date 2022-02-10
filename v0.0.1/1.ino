#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <NTPClient.h>               // Include NTPClient library
#include <TimeLib.h>                 // Include Arduino time library
#include <WiFiUdp.h>

const char* ssid = "TP-Link_AF84";               // Название Вашей WiFi сети
const char* password = "20000411lav";          // Пароль от Вашей WiFi сети

WiFiServer server(80);                                  // Указываем порт Web-сервера

WiFiUDP ntpUDP;
// 'time.nist.gov' is used (default server) with +1 hour offset (3600 seconds) 60 seconds (60000 milliseconds) update interval
NTPClient timeClient(ntpUDP, "time.nist.gov", 3600, 60000);
char Time[] = "TIME:00:00:00";
char Date[] = "DATE:00/00/2000";
byte last_second, second_, minute_, hour_, day_, month_;
int year_;

void setup() 
{
  Serial.begin(115200);                                 // Скорость передачи 115200 
  delay(10);                                            // Пауза 10 мкс
                             
  Serial.println("");                                   // Печать пустой строки 
  Serial.print("Connecting to ");                       // Печать "Подключение к:"
  Serial.println(ssid);                                 // Печать "Название Вашей WiFi сети"
  
  WiFi.begin(ssid, password);                           // Подключение к WiFi Сети
  
  while (WiFi.status() != WL_CONNECTED)                 // Проверка подключения к WiFi сети
  {
   delay(500);                                          // Пауза 500 мкс
   Serial.print(".");                                   // Печать "."
  }
   Serial.println("");                                  // Печать пустой строки                                          
   Serial.println("WiFi connected");                    // Печать "Подключение к WiFi сети осуществлено"
   server.begin();                                      // Запуск Web сервера
   Serial.println("Web server running.");               // Печать "Веб-сервер запущен"
   delay(10000);                                        // Пауза 10 000 мкс
   Serial.println(WiFi.localIP());                     // Печатаем полученный IP-адрес ESP
   timeClient.begin();
}

void loop() 
{
 pinMode(2, INPUT);
 WiFiClient client = server.available();                // Получаем данные, посылаемые клиентом 
 timeClient.update();
 unsigned long unix_epoch = timeClient.getEpochTime();    // Get Unix epoch time from the NTP server
 
 second_ = second(unix_epoch);
 if (client){
  Serial.println("New client");                         // Отправка "Новый клиент"
  boolean blank_line = true;                            // Создаем переменную, чтобы определить конец HTTP-запроса 
  while (client.connected()){                           // Пока есть соединение с клиентом 
    if (client.available()){                            // Если клиент активен 
     char c = client.read();                            // Считываем посылаемую информацию в переменную "с"
     if (c == '\n' && blank_line){                      // Вывод HTML страницы 
       client.println("HTTP/1.1 200 OK");               // Стандартный заголовок HTTP 
       client.println("Content-Type: text/html"); 
       client.println("Connection: close");             // Соединение будет закрыто после завершения ответа
       client.println("Refresh: 5");                   // Автоматическое обновление каждые 10 сек 
       client.println();
       client.println("<!DOCTYPE HTML>");               // Веб-страница создается с использованием HTML
       client.println("<html>");                        // Открытие тега HTML 
       client.println("<head>");
       client.print("<title>ESP8266 TEMP</title>");     // Название страницы
       client.println("</head>");
       client.println("<body>");
       client.println("<h1>ESP8266 </h1>");
       
       if (digitalRead(2) == HIGH){
         if (last_second != second_) {
 
    minute_ = minute(unix_epoch);
    hour_   = hour(unix_epoch);
    day_    = day(unix_epoch);
    month_  = month(unix_epoch);
    year_   = year(unix_epoch);
 
    Time[12] = second_ % 10 + 48;
    Time[11] = second_ / 10 + 48;
    Time[9]  = minute_ % 10 + 48;
    Time[8]  = minute_ / 10 + 48;
    Time[6]  = hour_   % 10 + 48;
    Time[5]  = hour_   / 10 + 48;
 
    Date[5]  = day_   / 10 + 48;
    Date[6]  = day_   % 10 + 48;
    Date[8]  = month_  / 10 + 48;
    Date[9]  = month_  % 10 + 48;
    Date[13] = (year_   / 10) % 10 + 48;
    Date[14] = year_   % 10 % 10 + 48;
       }
    last_second = second_;
        client.println("<h3>There is movement!</h3>");
        client.println(Time);
        client.println(Date);
       } else {
         if (last_second != second_) {
 
    minute_ = minute(unix_epoch);
    hour_   = hour(unix_epoch);
    day_    = day(unix_epoch);
    month_  = month(unix_epoch);
    year_   = year(unix_epoch);
 
    Time[12] = second_ % 10 + 48;
    Time[11] = second_ / 10 + 48;
    Time[9]  = minute_ % 10 + 48;
    Time[8]  = minute_ / 10 + 48;
    Time[6]  = hour_   % 10 + 48;
    Time[5]  = hour_   / 10 + 48;
 
    Date[5]  = day_   / 10 + 48;
    Date[6]  = day_   % 10 + 48;
    Date[8]  = month_  / 10 + 48;
    Date[9]  = month_  % 10 + 48;
    Date[13] = (year_   / 10) % 10 + 48;
    Date[14] = year_   % 10 % 10 + 48;
       }
    last_second = second_;
        client.println("<h3>No movement :(</h3>");
        client.println(Time);
        client.println(Date);
       }
       
       client.println("</body>");
       client.println("</html>");                       // Закрытие тега HTML 
       break;                                           // Выход
       }
        if (c == '\n'){                                 // Если "с" равен символу новой строки                                             
         blank_line = true;                             // Тогда начинаем новую строку
        }                                          
         else if (c != '\r'){                           // Если "с" не равен символу возврата курсора на начало строки                                        
          blank_line = false;                           // Тогда получаем символ на текущей строке 
         }                                        
    }
  }  
    client.stop();                                      // Закрытие соединения
    Serial.println("Client disconnected.");             // Печать "Клиент отключен"

 }
}
