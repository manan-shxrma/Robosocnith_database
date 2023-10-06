double ch1 = 0;
double ch2 = 0;
double ch3 = 0;
int R_EN = 2;
int R_PWM =3;

int L_EN = 7;
int L_PWM = 8;

int attackmotor1=5;
int attackmotor2=6;

void setup()
{
  Serial.begin(9600);

  pinMode(R_EN, OUTPUT);
  pinMode(R_PWM, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(L_PWM, OUTPUT);
  pinMode (attackmotor1,OUTPUT);
  
   pinMode (attackmotor2,OUTPUT); 
   pinMode(11, INPUT); 
  pinMode(10, INPUT);
  pinMode(9, INPUT);
}

void loop()
{

  ch1 = pulseIn(10, 255);
  ch2 = pulseIn(9, 255);
    ch3 = pulseIn(11, 255);
  if ((ch1 == 0) && (ch2 == 0))
  {

    analogWrite(L_PWM, 0); analogWrite(R_PWM, 0);
    analogWrite(L_EN, 0); analogWrite(R_EN, 0);

  }

  else if ((ch1 > 1530) && (ch2 > 1530) )
  {
    analogWrite(L_PWM, 255);
    analogWrite(L_EN, 0);

    analogWrite(R_PWM, 0);
    analogWrite(R_EN, 255);
  }

  else if ((ch1 > 1530) && (ch2 < 1460))
  {
    analogWrite(L_PWM, 0);
    analogWrite(L_EN, 255);

    analogWrite(R_PWM, 0);
    analogWrite(R_EN, 255);

  }

  else if ((ch1 < 1460) && (ch2 > 1530))
  {
    analogWrite(L_PWM, 255);
    analogWrite(L_EN, 0);

    analogWrite(R_PWM, 255);
    analogWrite(R_EN, 0);
  }

  else if ((ch1 < 1460) && (ch2 < 1460))
  {
    analogWrite(L_PWM, 0);
    analogWrite(L_EN, 255);

    analogWrite(R_PWM, 255);
    analogWrite(R_EN, 0);

  }


  else
  {
    analogWrite(L_PWM, 0); analogWrite(R_PWM, 0);
    analogWrite(L_EN, 0); analogWrite(R_EN, 0);
  }
       if ((ch3 > 1700))
  {
    analogWrite(attackmotor1, 0);
    analogWrite(attackmotor2, 255);

  }
       else if  ((ch3 > 1500) && (ch3<1700))
  {
    analogWrite(attackmotor1, 0);
    analogWrite(attackmotor2, 170);

  }

         else if  ((ch3 > 1200) && (ch3<1500))
  {
    analogWrite(attackmotor1, 0);
    analogWrite(attackmotor2, 100);

  }
  
      else if  ((ch3 < 1500))
  {
    analogWrite(attackmotor1, 0);
    analogWrite(attackmotor2, 0);

  }
  

}