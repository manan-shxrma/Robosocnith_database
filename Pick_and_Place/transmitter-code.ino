#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(9,8); // CE, CSN
const byte address[6] = "00001  ";
char xyData[32] = "";
int joystick[4];

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.stopListening();
}
void loop() {
 
  joystick[0] = analogRead(A1);
  joystick[1] = analogRead(A2);
  joystick[2] = analogRead(A0);
  joystick[3] = analogRead(A3);

  Serial.println(joystick[0]);
  Serial.println(joystick[1]);
  Serial.println(joystick[2]);
  Serial.println(joystick[3]);
  
  radio.write( &joystick, sizeof(joystick) );
}