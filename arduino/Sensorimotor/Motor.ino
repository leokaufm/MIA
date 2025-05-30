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

/* void panel1(){
  panel 1 - waking up/greeting
  
} 

void panel2(){
  // panel 2 - Curiosity
    moveBoth(100); // approach
    delay(1000);
    stopBoth();
    delay(100);

    moveHead(40); // tilt head to left
    delay(80);
    stopHead(); // stop head, questioning look 
    delay(2000);
    moveHead(-40); // move head back
    delay(115);
    stopHead();
    delay(500);
}

void panel3(){
  // Panel 3 - Excitement
  moveBoth(-100); // retreat a little
  delay(1500);
  stopBoth();
  delay(2000);

  turnRight(200); // 360 turn to the right
  delay(2000);
  stopBoth();

  turnLeft(200); // 360 turn to the left
  delay(1800);
  stopBoth();
}

void interaction_sequence(){
  panel1();
} */

// void stopReels() {
//   moveReels(0);
// }

// void moveReels(int speed) {
//   if (speed == 0) {
//     leftReel->run(RELEASE);
//     rightReel->run(RELEASE);
//   } else {
//     leftReel->setSpeed(speed);
//     rightReel->setSpeed(speed);
//     if (speed > 0) {
//       rightReel->run(FORWARD);
//       leftReel->run(FORWARD);    
//     } else {
//       rightReel->run(BACKWARD);
//       leftReel->run(BACKWARD);
//     }
//   }    
// }
