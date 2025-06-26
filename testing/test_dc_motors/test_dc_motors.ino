#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);

bool done =false;

void setup() {
  Serial.begin(9600);  
  while (!Serial);
  Serial.println("Running motor...");

  AFMS.begin(1000);  // Default 1.6KHz     
}

void loop() {
  if (!done){
    leftMotor->setSpeed(150);
    rightMotor->setSpeed(150);
    leftMotor->run(BACKWARD);
    rightMotor->run(BACKWARD);
    delay(700);
    leftMotor->run(RELEASE);
    rightMotor->run(RELEASE);
    done = true;
  }
}
