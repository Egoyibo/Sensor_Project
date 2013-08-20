// The aim of this sketch is to successfully pass 1s or 0s from
// the arduino to my pyserial file

/*
  STEPSSSSSSS
  - Use a button, and while it's pressed down, calculate average 
    of irms
*/

#include "EmonLib.h"
EnergyMonitor emon;

// First declare constants
const int buttonPin = 2;

int buttonState = 0;


// Variable to store my avg
int avgirms = -1;
int sumirms = 0;
int count = 0;
char *curr_state = "Off";
char *prev_state = "Off";
int power;




// Setup
void setup()
{
  Serial.begin(9600);  emon.current(1, 111.1);     //Current: input pin, calibration.
  pinMode(buttonPin, INPUT);  //Initialize the button as an input
  double Irms = emon.calcIrms(1480);
  delay(1000);
}






void loop()
{
  int Irms = emon.calcIrms(1480) * 100;
  //Serial.println("IRMS: ");
  //Serial.println(Irms);
  buttonState = digitalRead(buttonPin);
  //double Irms = emon.calcIrms(1480);
//  Serial.println(Irms);
  
 // Try 4
  if (buttonState == HIGH)
  {
    sumirms = sumirms + Irms;
    count = count + 1;
    avgirms = sumirms/count;
    //Serial.print("Avg Irms: ");
    //Serial.println(avgirms);
  }
  if (avgirms != -1 && (Irms - avgirms) > 0)
  {
  power = (Irms-avgirms)*120; //Apparent Power
  Serial.println(power);
  }
  
  if (avgirms != -1 && abs(Irms - avgirms) > 10) {
    //Serial.print("Irms: ");
    //Serial.print(Irms);
    //Serial.print("State: ");
    //Serial.println("On");
    curr_state = "On";
  }
  else if (avgirms != -1 && abs(Irms - avgirms) < 10) {
    //Serial.print("Irms: ");
    //Serial.print(Irms);
    //Serial.print("State: ");
    //Serial.println("Off");
    power = 0;
    curr_state = "Off";
  }
  
  if (curr_state != prev_state){
    //Serial.print("Boo-Yah!!!");
    //Serial.println(Irms * 120); //Apparent Power
    //Serial.println(power);
    Serial.println(curr_state);
  }
  
  prev_state = curr_state;
}