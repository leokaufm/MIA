# MIA
Movent to Inspire Affection. Code for a robot pet interacting with children.

## Hardware
The robot has two driving wheels powered by two Makeblock Optical Encoder Motors-25
9V/86rpm and a free caster wheel for support. A third motor moves the head of the robot in a
rolling motion. Two entities are used to control the robot. The primary control loop is realized
by an Arduino Uno microcontroller with a mounted Adafruit Motor Shield v2.3. An HC-SR04
ultrasonic sensor for measuring distances to objects is linked to the Arduino. The Arduino is
connected in series to a Raspberry Pi 4 Model B single-board computer (SBC) that serves
for communication with a computer via WiFi. On the Raspberry Pi, a Raspberry Pi Camera
V2.1 is mounted. To power the Raspberry Pi, a Ditron power bank model SK-Pw1 with a
total output of 4.2A at 5V is used. The Arduino, the motors, and the ultrasonic sensor are
powered by a lithium polymer 11.1V battery.

## Software
For the software, code in Python 3.7 is used for the Raspberry Pi, and the C/C++ based
Arduino Programming Language for the Arduino. In the code on the Raspberry Pi, a
connection with an external computer that serves as the remote control entity for the robot
via WiFi is established using UDP protocol. Commands for going forward, backward, turning,
and moving the head are sent to the robot in the form of keyboard presses. With another
command, the camera is activated. The video is transmitted via UDP protocol to the computer.
A live stream is started on the remote computer, and the video is stored for later use. In the
code on the Arduino, the commands are received, and the corresponding motors are driven.
The Arduino receives data from the ultrasonic sensor and drives the wheel motors backward
as soon as an object is detected within a threshold distance.

# Media
Based on: * https://www.youtube.com/watch?v=FxIlZGT8ktU
