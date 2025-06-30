void move(Adafruit_DCMotor * motor, int speed) {
  if (motor == rightMotor)
    botState.rightSpeed = speed;
  else
    botState.leftSpeed = speed;

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

void moveBoth(int speed) {
  moveLeft(speed);
  moveRight(speed);
}

void turnRight(int speed) {
  moveLeft(-speed);
  moveRight(speed);
}

void turnLeft(int speed) {
  moveLeft(speed);
  moveRight(-speed);
}

void stopLeft() {
  move(leftMotor, 0);
}

void stopRight() {
  move(rightMotor, 0);
}

void stopBoth() {
  stopLeft();
  stopRight();
}

void moveHead(int speed) {
  botState.headSpeed = speed;
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

void interaction(){
  delay(2000); // wait shortly before starting

  moveBoth(-80); // wiggle back and forth
  delay(150);
  moveBoth(80);
  delay(150);
  moveBoth(-80);
  delay(150);
  stopBoth();
  delay(500);

  moveBoth(-80); // wiggle back and forth
  delay(150);
  moveBoth(80);
  delay(150);
  moveBoth(-80);
  delay(150);
  stopBoth();
  delay(2000);

  turnLeft(80); // wiggle sideways
  delay(150);
  stopBoth();
  turnRight(80);
  delay(150);
  stopBoth();
  turnLeft(80);
  delay(150);
  stopBoth();
  turnRight(80);
  delay(150);
  stopBoth();
  delay(2000);

  turnLeft(100); // turn left 90 degrees
  delay(900);
  stopBoth();
  delay(2000);

  moveBoth(100); // approach
  delay(1000);
  stopBoth();
  delay(2000);

  moveHead(-40); // tilt head to the right
  delay(120);
  stopHead(); // stop head, questioning look 
  delay(3000);
  moveHead(40); // move head back
  delay(110);
  stopHead();
  delay(500);

  moveBoth(-100); // retreat
  delay(1000);
  stopBoth();
  delay(2000);

  turnRight(100); // turn right 90 degrees
  delay(900);
  stopBoth();
  delay(2000);
}


