#include <Adafruit_MotorShield.h>
#include "Wire.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);
Adafruit_DCMotor *head = AFMS.getMotor(3);

int count = 0;
bool done = false;

void moveHead(int speed) {
  //botState.headSpeed = speed;
  if (speed == 0){
    head->run(RELEASE);
  } else {
    head->setSpeed(abs(speed));
    if (speed > 0) {
      head->run(BACKWARD);
    } else {
      head->run(FORWARD);
    }
  }
}

void stopHead() {
  moveHead(0);
}

void move(Adafruit_DCMotor * motor, int speed) {
  /* if (motor == rightMotor)
    botState.rightSpeed = speed;
  else
    botState.leftSpeed = speed; */

  if (speed == 0) {
    motor->run(RELEASE);
  } else {
    motor->setSpeed(abs(speed));
    if (speed > 0) {
      motor->run(BACKWARD);
    } else {
      motor->run(FORWARD);
    }
  }    
}

void moveLeft(int speed) {
  move(leftMotor, speed);
}

void moveRight(int speed) {
  move(rightMotor, speed);
}

void stopLeft() {
  move(leftMotor, 0);
}

void stopRight() {
  move(rightMotor, 0);
}

void moveBoth(int speed){
  moveRight(speed);
  moveLeft(speed);
}

void stopBoth(){
  moveRight(0);
  moveLeft(0);
}

void turnLeft(int speed){
  moveLeft(-speed);
  moveRight(speed);
}

void turnRight(int speed){
  moveLeft(speed);
  moveRight(-speed);
}

void setup() {
  Serial.begin(9600);
  delay(2000);
  Serial.flush();
  Serial.println("Interaction test");
  
  AFMS.begin();  // Start motor shield
  //leftMotor->setSpeed(100);
  //rightMotor->setSpeed(100);
  //head->setSpeed(100);  // Adjust speed (0–255)
}

void loop() {
  if (!done){
    delay(5000); //debug

    moveBoth(100); // move out of box
    delay(1500);
    stopBoth();
    delay(2000);

    moveBoth(-100); // wiggle back and forth
    delay(150);
    moveBoth(100);
    delay(150);
    moveBoth(-100);
    delay(150);
    stopBoth();
    delay(2000);

    turnLeft(100); //turn left 90 degrees
    delay(900);
    stopBoth();
    delay(2000);

    moveBoth(100); // approach
    delay(1000);
    stopBoth();
    delay(2000);

    moveHead(40); // tilt head to left
    delay(80);
    stopHead(); // stop head, questioning look 
    delay(3000);
    moveHead(-40); // move head back
    delay(80);
    stopHead();
    delay(500);

    moveBoth(-100); // retreat
    delay(1000);
    stopBoth();
    delay(2000);

    turnRight(100); //turn right 90 degrees
    delay(900);
    stopBoth();
    delay(2000);

    /* turnLeft(100); //turn left joy
    delay(2000);
    stopBoth();
    delay(2000);

    turnRight(100); //turn right joy
    delay(2000);
    stopBoth();
    delay(2000); */

    moveBoth(-100); // move back into box
    delay(1500);
    stopBoth();
    delay(2000);

    done = true;
  }
}
