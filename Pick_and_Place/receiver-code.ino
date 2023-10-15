#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>
#define enA A1 
#define in1 7
#define in2 6
#define enB A2   
#define in3 5
#define in4 4
Servo myservo;
Servo myservotwo;
RF24 radio(9,8); // CE, CSN
const byte address[6] = "00001";
char receivedData[32] = "";
int  xAxis, yAxis, zAxis, wAxis;
int motorSpeedA = 0;
int motorSpeedB = 0;
int motorSpeedC = 0;
int motorSpeedD = 0;
int joystick[4]; 
 
void setup() {
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  myservo.attach(10);
  myservotwo.attach(3);

  Serial.begin(9600);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
  
 
}
void loop() {
 
  if (radio.available()) {   // If the NRF240L01 module received data
     
      radio.read( &joystick, sizeof(joystick) );
  radio.read(&receivedData, sizeof(receivedData));
    yAxis = joystick[0];
    xAxis = joystick[1];
    zAxis = joystick[2];
    wAxis = joystick[3];
    Serial.println(yAxis);
    Serial.println(xAxis);
    Serial.println(zAxis);
    Serial.println(wAxis); 
  }
  
  if (yAxis < 470) {
 
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
 
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
 
    motorSpeedA = map(yAxis, 470, 0, 0, 255);
    motorSpeedB = map(yAxis, 470, 0, 0, 255);
  }
  else if (yAxis > 550) {
 
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
 
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    
    motorSpeedA = map(yAxis, 550, 1023, 0, 255);
    motorSpeedB = map(yAxis, 550, 1023, 0, 255);
  }
 
  else {
    motorSpeedA = 0;
    motorSpeedB = 0;
  }
 
  if (xAxis > 550) {
    
     digitalWrite(in1,HIGH);
    digitalWrite(in2, LOW);
 
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    
    motorSpeedA = map(xAxis, 550, 1023, 0, 255);
    motorSpeedB = map(xAxis, 550, 1023, 0, 255);
    if (motorSpeedA < 0) {
      motorSpeedA = 0;
    }
    if (motorSpeedB > 255) {
      motorSpeedB = 255;
    }
  }
  if (xAxis < 470) {
    
     digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
 
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    
    motorSpeedA = map(xAxis, 470, 0, 0, 255);
    motorSpeedB = map(xAxis, 470, 0, 0, 255);
    
    if (motorSpeedA > 255) {
      motorSpeedA = 255;
    }
    if (motorSpeedB < 0) {
      motorSpeedB = 0;
    }
  }
  
  if (motorSpeedA < 70) {
    motorSpeedA = 0;
  }
  if (motorSpeedB < 70) {
    motorSpeedB = 0;
  }
  analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
  analogWrite(enB, motorSpeedB); // Send PWM signal to motor B

  motorSpeedC = map(zAxis, 0, 1023, 0, 180);
   myservo.write(motorSpeedC);

  motorSpeedD = map(wAxis, 0, 1023, 0, 180);
  myservotwo.write(motorSpeedD);  
  
}