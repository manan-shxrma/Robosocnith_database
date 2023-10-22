#include <SoftwareSerial.h>
SoftwareSerial mySerial(7, 8);

void setup()
{
  mySerial.begin(9600);   // Setting the baud rate of GSM Module  
  Serial.begin(9600);    // Setting the baud rate of Serial Monitor (Arduino)
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
}

void loop()
{
  if (mySerial.available()>0)
    Serial.write(mySerial.read());
    
  if (Serial.available()>0)
    mySerial.write(Serial.read());
    
  if(mySerial.available()>0){
    String message = mySerial.readString();
    if(message.indexOf("ON")>=0){
      digitalWrite(13, HIGH);
      mySerial.println("LED is ON");
    }
    else if(message.indexOf("OFF")>=0){
      digitalWrite(13, LOW);
      mySerial.println("LED is OFF");
    }
  }
}
