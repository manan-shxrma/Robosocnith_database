#include <QTRSensors.h>
#define left_motor_positive 7
#define left_motor_negative 6
#define right_motor_positive 8
#define right_motor_negative 9
#define en1 10
#define en2 5

int check = 0;
int attempt = 0;
int rightState =0;

int w = 400;
int b = 900;
int c = 500;

#define led 13


QTRSensors qtra;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];





int initial_motor_speed = 70;
int rotating_speed = 30;//60
int forward_speed = 90;
int right_motor_speed = 0; //for the speed after PID control
int left_motor_speed = 0;


int error; 
float kp = 0.25; //proportiona constant
float ki = 0;
float kd = 0.75;
float P,I,D,previousError=0;
int pid_value;

char mode;
int Status = 0;
int buttom_reading;

int ObstaclePin=10;
int ObstacleRead;
void led_signal(int times);

void calculatePID();
void PIDmotor_control();
   uint16_t position;

void readIRvalue();     //to read sensor value and calculate error as well mode
// void Set_motion();

void dryrun();
// void actualrun();

void recIntersection(char);
char path[100] = "";
unsigned char pathLength = 0; // the length of the path
int pathIndex = 0;
// void setmotionactual();
// void mazeTurn (char dir);

void forward(int spd1, int spd2);
void left(int spd);
void right(int spd);
void stop_motor();
void goAndTurnLeft();
void maze_end();
void move_inch();
void backward(int spd1, int spd2);


void setup() 
{ 
 Serial.begin(9600);
  // put your setup code here, to run once:
  for (int i = 2; i <= 5; i++)
  {
    pinMode(i, OUTPUT);
  }
  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);
  digitalWrite(left_motor_positive, LOW);
  digitalWrite(left_motor_negative, LOW);
  digitalWrite(right_motor_positive, LOW);
  digitalWrite(right_motor_negative, LOW);
  digitalWrite(led, LOW);
  delay(500);
  pinMode(13, OUTPUT);

  qtra.setTypeAnalog();
  qtra.setSensorPins((const uint8_t[]){A0, A1, A2, A3, A4, A5, 11,3}, SensorCount);
  qtra.setEmitterPin(9);

  
  digitalWrite(13, HIGH);  

  
 // turn on Arduino's LED to indicate we are in calibration mode
  for (int i = 0; i < 300; i++)  // make the calibration take about 10 seconds
  {
    qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
  }
  digitalWrite(13, LOW);     // turn off Arduino's LED to indicate we are through with calibration

  // print the calibration minimum values measured when emitters were on

  
}


void loop() 
{   
    dryrun();
    delay(100);
 
  }


void led_signal(int times)
{
  for (int i = 0; i <= times; i=i+1)
  {
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    delay(100);
  }
}

//dryrun begins------------------------------------------------------------------------------------------------------------------
void dryrun()
{
     readIRvalue();
     set_motion();
  
}
//ReadIRvalue begins----------------------------------------------------------------------------------------------------------------------------------
void readIRvalue()
{
    uint16_t position = qtra.readLineBlack(sensorValues);
    
    error = 3500 - position;
      for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(sensorValues[i]);
    Serial.print("  ");
  }
  Serial.println(position);

    


//--------------------------------------------------------------------------------------
  if (sensorValues[0] < w && sensorValues[1] < w && sensorValues[2] < w && sensorValues[3] < w && sensorValues[4] < w && sensorValues[5] < w && sensorValues[6] < w && sensorValues[7] < w)
  {
    mode = 'N';  //NO LINE
    error = 0;
        Serial.println("N");

  }
  //--------------------------------------------------------------------------------------commented earlier
else if ( sensorValues[0] < w && sensorValues[1] < w && sensorValues[2] < w && sensorValues[3] < w && sensorValues[4] < w && sensorValues[5] < w && sensorValues[6] < w && sensorValues[7] < w)
 {
   mode = 'S';//Stop Condition
   error = 0;
       Serial.println("S");
 }
  //--------------------------------------------------------------------------------------

 

 else if ( sensorValues[0] < w && sensorValues[1] < w && sensorValues[6] > b  && sensorValues[7] > b)
 {
   mode = 'R';//90 degree turn
   error = 0;
 }

  
    else{
    mode = 'F';
    }
    Serial.println(mode);
     //mode = 'F';
}



//set motion begins------------------------------------------------------------------------------------------------------------------------------
void set_motion()
{
  switch (mode)
  {
    case 'N':
      stop_motor();
      goAndTurnRight();
      recIntersection('B');
      break;
    case 'S':
      move_inch();
      readIRvalue();
      if (mode == 'S')
      {
        maze_end();
      }
      else
      {
        goAndTurnLeft();
        recIntersection('L');
      }
      break;
    case'R':
      move_inch();
//      readIRvalue();
//      if (mode == 'F')
//      {
//        recIntersection('S');
//      }
//      else
//      {
          goAndTurnRight();
//      }
      break;
    case 'L':
      move_inch();
      goAndTurnLeft();
      break;
    case 'F':
      calculatePID();
      PIDmotor_control();
      break;
  }
}

//-----------------------------------------------------------------------------------------------------------
void move_inch()
{
  forward(forward_speed, forward_speed);
  delay(200);
  stop_motor();
}
//----------------------------------------------------------------------------------------------------------

void stop_motor()
{
  analogWrite(en1, 0);
  analogWrite(en2, 0);
  digitalWrite(left_motor_positive, LOW);
  digitalWrite(left_motor_negative, LOW);
  digitalWrite(right_motor_positive, LOW);
  digitalWrite(right_motor_negative, LOW);
  digitalWrite(led, LOW);
}
//-----------------------------------------------------------------------------------------------------------
void goAndTurnLeft()
{ 
    previousError = 0;
  left(rotating_speed);
  delay(100);
  do
  {
    left(rotating_speed);
    readIRvalue();
  } while (mode =! 'F'  && position < 2500);
  for(int i = 0; i < 100; i++){
    mode = 'F';
  }
}

//------------------------------------------------------------------------------------------------
void goAndTurnRight()
{previousError = 0;
  right(rotating_speed);
  delay(100);
  do
  {
    right(rotating_speed);
    readIRvalue();
  }while (mode != 'F' || position > 3900); 
  for(int i = 0; i < 100; i++){
    mode = 'F';
  }
}
//-----------------------------------------------------------------------------------------------
void maze_end()
{
  Status++;
  stop_motor();
  led_signal(20);
}
//------------------------------------------------------------------------------------------------
void calculatePID()
{
  
  P = error;
  I = I + error;
  D = error-previousError;
  pid_value = (kp*P) + (ki*I) + (kd*D);
  previousError = error;
  
}
//-----------------------------------------------------------------------------------------------
void PIDmotor_control()
{
  right_motor_speed = initial_motor_speed - pid_value;
  left_motor_speed = initial_motor_speed + pid_value;
  right_motor_speed = constrain(right_motor_speed, 0, initial_motor_speed);
  left_motor_speed = constrain(left_motor_speed, 0, initial_motor_speed);
  forward(left_motor_speed, right_motor_speed);
  
}

//-------------------------------------------------------------------------------------------------------
void forward(int spd1, int spd2)
{
  analogWrite(en1, spd1);
  analogWrite(en2, spd2);
  digitalWrite(left_motor_positive, HIGH);
  digitalWrite(left_motor_negative, LOW);
  digitalWrite(right_motor_positive, HIGH);
  digitalWrite(right_motor_negative, LOW);
  digitalWrite(led, LOW);
}

void backward(int spd1, int spd2)
{
  analogWrite(en1, spd1);
  analogWrite(en2, spd2);
  digitalWrite(left_motor_positive, HIGH);
  digitalWrite(left_motor_negative, LOW);
  digitalWrite(right_motor_positive, HIGH);
  digitalWrite(right_motor_negative, LOW);
  digitalWrite(led, HIGH);
}

void left(int spd)
{
  analogWrite(en1, spd);
  analogWrite(en2, spd);
  digitalWrite(left_motor_positive, HIGH);
  digitalWrite(left_motor_negative, LOW);
  digitalWrite(right_motor_positive, LOW);
  digitalWrite(right_motor_negative, HIGH);
  digitalWrite(led, HIGH);
}

void right(int spd)
{
  analogWrite(en1, spd);
  analogWrite(en2, spd);
  digitalWrite(left_motor_positive, LOW);
  digitalWrite(left_motor_negative, HIGH);
  digitalWrite(right_motor_positive, HIGH);
  digitalWrite(right_motor_negative, LOW);
  digitalWrite(led, HIGH);
}
//--------------------------------------------------------------------------------------


void recIntersection(char Direction)
{
    Serial.println(Direction);
}