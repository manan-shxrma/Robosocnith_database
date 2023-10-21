#include <Wire.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(22,24);
#define echoPin 8 
#define trigPin 9 
#define buzzer  4


// defines variables
long duration;
int distance;
int count = 0;
int motor1Pin1  = 5;
int motor1Pin2 = 6;
int motor2Pin1 = 2;
int motor2Pin2 = 3;
int en1 = 10;
int en2 = 11;


void moveF(){
  analogWrite(en1, 70);
  analogWrite(en2, 70);
  digitalWrite(motor1Pin1 , LOW);
  digitalWrite(motor1Pin2 , HIGH);
  digitalWrite(motor2Pin1 , HIGH);
  digitalWrite(motor2Pin2 , LOW);
}
void moveB(){
  analogWrite(en1, 70);
  analogWrite(en2, 70);
  digitalWrite(motor1Pin1 , HIGH);
  digitalWrite(motor1Pin2 , LOW);
  digitalWrite(motor2Pin1 , LOW);
  digitalWrite(motor2Pin2 , HIGH);
}
void stopF(){
  digitalWrite(motor1Pin1 , LOW);
  digitalWrite(motor1Pin2 , LOW);
  digitalWrite(motor2Pin1 , LOW);
  digitalWrite(motor2Pin2 , LOW);
}
void setup() {
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
  pinMode(buzzer, OUTPUT);
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
  Serial.begin(9600);
  Wire.begin();
  mySerial.begin(9600); 
}
void loop() {
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW); 
      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2; 
      Serial.print("Distance: ");
      Serial.println(distance);
      if(distance>3){//distance is 3cm actually
          stopF();
          digitalWrite(buzzer,LOW);
          delay(2000);
          if(mySerial.available()>0){
          mySerial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
          delay(1000);  // Delay of 1000 milli seconds or 1 second
          mySerial.println("AT+CMGS=\"+911234567890\"\r"); // Replace with your mobile number
          delay(2000);
          mySerial.println("Crack Detected");// The SMS text you want to send
          delay(100);
          mySerial.println((char)26);// ASCII code of CTRL+Z
          }
          delay(1000);
          moveF();          
      }
      else{
        digitalWrite(buzzer,HIGH);        
      }
    //delay(2000);
    moveF();
    Serial.println(" cm");
}