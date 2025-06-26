/**
 * Bot
 */

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "MeMCore.h"
#include <SoftwareSerial.h>

//#define sigPin 3
MeUltrasonicSensor ultraSensor(PORT_3);

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Motors with Adafruit library
Adafruit_DCMotor *rightMotor = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(2);
Adafruit_DCMotor *head = AFMS.getMotor(3);
// Adafruit_DCMotor *rightReel = AFMS.getMotor(4);

// Distance sensor
#define trigPin 2
#define echoPin 3

bool debug = false;
bool debugSensor = false;
String codeversion="1.0";

struct sensortype
{
  long code;
  long rightEncoder;
  long leftEncoder;
  long headEncoder;
  float voltage;
  float current;
  long freq;
  long counter;
  int distance;
} sensor;

struct botStateType {
  long leftSpeed;
  long rightSpeed;
  long headSpeed;
} botState;

int StateMachine(int state, int controlvalue)
{
  static int previousState = 0;
  switch (state)
  {
    case 0x01: // left motor forward
      moveLeft(controlvalue);
      break;
    case 0x02: // right motor forward
      moveRight(controlvalue);
      break;
    case 0x03: // left motor backwards
      moveLeft(-controlvalue);
      break; 
    case 0x04: // right motor backwards
      moveRight(-controlvalue);
      break;   
    case 0x05: // both motors forward
      moveRight(controlvalue);
      moveLeft(controlvalue);
      break;  
    case 0x06: // both motors backwards
      moveRight(-controlvalue);
      moveLeft(-controlvalue);
      break;  
    case 0x07: // stop both motors
      stopLeft();
      stopRight();
      break;
    case 0x08: // interaction sequence
      interaction();
      break;
    case 0x0A: // tilt head to the left
      moveHead(-controlvalue);
      break;   
    case 0x0B: // tilt head to the right
      moveHead(controlvalue);
      break;
    case 0x0C: // stop head
      stopHead();
      break;
    case 0x0F: // stop all motors and reels
      stopRight();
      stopLeft();
      stopHead();
      break;
    default:
      // Do Nothing
      state = 0;
      break;
  }  
  
  previousState = state;
  return state;
}

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.print("MIA v");Serial.println(codeversion);
  stopBurst();
    
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  moveLeft(1);
  stopLeft();

  moveRight(1);
  stopRight();

  moveHead(1);
  stopHead();

  memset(&sensor, 0, sizeof(sensor));
  memset(&botState, 0, sizeof(botState));

  // botState.reelSpeed = 100;
  
  setupMotorEncoders();
  // setupReelEncoders();
}

int incomingByte = 0;

char buffer[6];
char actionBuf[3];

void readcommand(int &action, int &controlvalue)
{
  // Format ACCNNN, 'A', CC is command, NNN is the controlvalue.
  memset(buffer, 0, 6);
  memset(actionBuf, 0, 3);
  int readbytes = Serial.readBytes(buffer, 5);

  if (readbytes == 5) {
    actionBuf[0] = buffer[0];
    actionBuf[1] = buffer[1];
    
    action = strtol(actionBuf, NULL, 16);
    controlvalue = atoi(buffer + 2);
    
    if (debug) {
      Serial.print("Action:"); Serial.print(action); Serial.print("|"); Serial.println(controlvalue);
    }
  }
}

// the loop routine runs over and over again forever:
void loop() {
  // Ultrasonic sensor for distance:
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;
  sensor.distance = distance;
  if (distance == 0) {
    // This is likely an error with the sensor.
    //buzz();
    // Serial.print("Distance == 0, sensor error\n");
  } else if (distance < 12) {
    Serial.print("OBSTACLE !");Serial.println(distance);Serial.print("\n");
    moveBoth(-100);
    delay(200);
    stopBoth();
  } /* else {
    Serial.print("Distance > 12\n");
  } */

  // Control/command loop:
  unsigned long currentMillis = millis();
  int incomingByte;
  int action, state, controlvalue;
  
  /* sensor.freq = frequency();
  burstSensors(); */

  bool doaction = false;
  
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    doaction = true;
  }

  if (doaction) 
  {
    switch (incomingByte) {
      case 'D':
        debug = (!debug);
        break;
      case 'C': 
        debugSensor = (!debugSensor);
        break;
      // case 'R':
      //   autoretract = (!autoretract);
      //   if (!autoretract)
      //     stopReels();
      //   break;
      case 'A': // motor controls
        readcommand(action, controlvalue);
        state = action; // let StateMachine process the action
        break;
      case 'S': // sensor controls
        readcommand(action, controlvalue);
        state = 0;
        switch (action) {
          case 0x01:
            startBurst(controlvalue);
            break;
          case 0x02:
            stopBurst();
            break;
          case 0x1A:
            // Determines the amount of frames to send in a burst.
            setBurstSize(controlvalue);
            break;
          case 0x1B:
            // Determines the updating frequency in relation to current arduino frequency (which is variable)
            // For instance, 1 means the same frequency, 2 means half the frequency: 1/freq
            setUpdateFreq(controlvalue);
            break;
          case 0x1C:
            setCode(controlvalue);
            break;
          case 0x21:
            sendPayloadSize();
            break;
          case 0x22:
            transmitSensors();
            break;
          case 0x30:
            // Reset encoders
            resetEncoders();
            // resetReelEncoders();
            break;
        }
    }
  }

  StateMachine(state, controlvalue);
}
