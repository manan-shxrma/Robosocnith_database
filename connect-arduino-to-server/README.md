# Documentation for the crack detector bot with GSM module

## Project Overview
- This project aims to connect the arduino uno to a mongodb database using the server in between and ESP8266 module.
- We will create a server using node.js and express , connect it to the mongoDB database and then will write the data on the database using http requests made by arduino to the server using the ESP8266 module.
- This procedure then can be used to transmit values to the DB in different projects and use that data to make predictions.

## Hardware

### Componets Required 

1. Arduino Uno
2. ESP8266 module

## Software

### Libraries Used For Arduino
- ESP8266WiFi.h
- ESP8266HTTPClient.h

### Server Libraries/modules
- express
- mongoose
