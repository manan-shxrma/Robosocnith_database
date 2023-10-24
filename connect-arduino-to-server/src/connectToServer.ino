#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

#define url "http://example.com/data"
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST("{\"value\":123,\"timestamp\":\"2023-10-22T07:29:32Z\"}");
    String payload = http.getString();

    Serial.println(httpCode); 
    Serial.println(payload); 

    http.end();
  }

  delay(30000);
}
