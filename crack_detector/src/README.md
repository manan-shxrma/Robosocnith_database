# Documentation for the crack detector bot with GSM module

## Hardware

### Componets Required 

1. Ultrasonic sensor
2. Arduino Mega
3. Motor Driver
4. Li-ion Battery
5. Motors
6. Jumper wires
7. Chassis and wheels
8. GSM module
9. Buzzer
10. SIM Card

### Circuit Overview
- The arduino mega board is to be connected to the motor driver, gsm module and ultrasonic sensor.
- Motor Driver is connected to the motors to control the speed of the bot based on the controlling speeds sent to the motors by arduino mega using readings from ultrasonic sensor.
- GSM module is used to transmit the message of the crack to the user mobile.

## Software

### Libraries Used
- SoftwareSerial.h

### Algorithm 
- The ultrasonic sensor can provide value of distance of the ground from the bot, by sending the sound waves and measuring the distance to receive back those waves sent.
- If the distance > the normal distance b/w the bot and the ground then there is a crack at that place on rails/path.
- Once the crack is detected, buzzer is given signal to make a sound and gsm module is used to transmit the message of the crack at the path.

