import platform
import argparse
import fcntl
import time
import datetime
import sys
import os
import serial
import socket
import signal
import time

from connection import MCast
from connection import SerialConnection
from connection import Surrogator
from telemetry import TelemetryLoader
from motor.SerialMotor import SerialMotor
from motor.SerialHead import SerialHead
# from control import control_functions
import Configuration

### Functions ###
def remove_wt_and_exit(signum, frame):
  os.remove('running.wt')
  exit(0)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def timeout():
    print ('Sending a multicast update of my own ip address:'+myip)
    noticer.send()

# Stop all motors when process is killed
def terminate():
  print('Stopping ALPIBot')
  try:
    # motors.stop()
    # reels.stop()
    os.remove('running.wt')
  finally:
    print('ALPIBot has stopped.')
  exit(0)

def reset_sensors():
  connection.send(bytes('S30000', 'ascii'))

### Program ###
# Create a witness token to guarantee only one instance running
if (os.access("running.wt", os.R_OK)):
    print('Another instance is running. Cancelling.')
    quit(1)
runningtoken = open('running.wt', 'w')

signal.signal(signal.SIGINT, remove_wt_and_exit)
signal.signal(signal.SIGTERM, remove_wt_and_exit)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

runningtoken.write(st)
runningtoken.close()

""" parser = argparse.ArgumentParser()
parser.add_argument('--multicast', '-m', action='store_true')
args = parser.parse_args() """

# IP Broadcast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
# Remote controller server for BotController.py
print('Starting up Controller Server on 0.0.0.0, port 30001')
server_address = ('0.0.0.0', 30001)
sock.bind(server_address)
sur = Surrogator(sock)

if (Configuration.broadcast_IP):
    sock.setblocking(0)
    sock.settimeout(0.01)

noticer = MCast.Sender()

myip = get_ip_address('wlan0')

if (len(myip)>0):
    myip = myip
else:
    myip = 'None'

start = time.time()
print('Multicasting my own IP address: ' + myip)
while Configuration.broadcast_IP:
    noticer.send()
    try:
        data, address = sock.recvfrom(1)
        print(f"data, address: {data}, {address}")
        if (len(data) > 0):
            break
    except:
        data = None

    if (abs(time.time()- start) > 100):
        print('Giving up broadcasting ip... Lets get started.')
        break

if (Configuration.broadcast_IP):
    sock.setblocking(1)
    sock.settimeout(0)

""" if args.multicast:
  print('Multicasting my IP address...')
  while True:
    noticer.send()
    time.sleep(1)
    try:
      data, address = sock.recvfrom(1)
      print(len(data))
      if len(data) > 0:
        break
    except:
      pass
    if (abs(time.time()- start) > 30):
      print('Giving up broadcasting IP... Lets get started.')
      break """

# Camera Streaming
system_platform = platform.system()
if system_platform == "Darwin": # Mac
  import FFMPegStreamer as pcs
else: # Windows, Linux
  import H264Streamer as pcs

dosomestreaming = False

vst = pcs.H264VideoStreamer()
if dosomestreaming:
  try:
    vst.startAndConnect()
  except Exception as e:
    print('Error starting H264 stream thread:'+e)

# Motors and Reels connections
connection = SerialConnection()
motors = SerialMotor(connection=connection)
head = SerialHead(connection=connection)
#reels = SerialReel(connection=connection)

# Sensors - Telemetry
sensors = TelemetryLoader(connection)


signal.signal(signal.SIGINT, lambda signum, frame: terminate())
signal.signal(signal.SIGTERM, lambda signum, frame: terminate())

# Control Loop
print('ALPIBot ready to follow!')
autonomous = False
# control_strategies = {
#   'follow_and_turn': control_functions.follow_turn,
#   'rotate_and_go': control_functions.rotate_go
# }
# control_strategy = control_strategies['follow_and_turn']

stream_telemetry = True
AUTONOMOUS_SLEEP = 0.05
# Live
while True:
  try:
    data = ''
    # TCP/IP server is configured as non-blocking
    sur.getmessage()

    cmd = sur.command
    cmd_data, address = sur.data, sur.address
    print(f"cmd_data, address: {cmd_data}, {address}")
    # time.sleep(5)

    if autonomous and cmd == '':
      # Autonomous control
      time.sleep(AUTONOMOUS_SLEEP)
      sdata = sensors.poll(frequency = 1, length = 1, stream = stream_telemetry)
      """ [l_s, r_s] = control_strategy(sdata)
      motors.left(l_s)
      motors.right(r_s) """
      # print([l_s, r_s])

    elif cmd == 'A':
      if (len(sur.message) == 5):
        # Sending the message that was received.
        print(sur.message)
        connection.send(sur.message)
        sur.message = ''

    elif cmd == 'U':
      if cmd_data == 'X':
        break

      if cmd_data == 'M': # Enable/disable autonomous command
        autonomous = not autonomous
        reset_sensors()
        if autonomous:
          print('Auto mode: ON')
        else:
          print('Auto mode: OFF')
      
        # Control strategies for autonomous mode -> undo indent when uncommenting
        """ elif cmd_data == '1':
          motors.stop()
          control_strategy = control_strategies['follow_and_turn']
          print('Control strat: Follow and Turn')
        elif cmd_data == '2':
          motors.stop()
          control_strategy = control_strategies['rotate_and_go']
          print('Control strat: Rotate and Go')
          
        elif cmd_data == 'R':  # Enable/disable autonomous reels
          connection.send(bytes('S1D250', 'ascii')) # Set reel speed to 250
          connection.send(bytes('R00000', 'ascii'))  # Enable auto reels
          print('Auto Reels toggle') """

      elif cmd_data == '0':
        reset_sensors()
      
      else: # Manual commands
        """ if cmd_data == 'k':
          reels.left(200)
        elif cmd_data == 'l':
          reels.right(200)
        elif cmd_data == 'r':
          reels.both(200) """
        if cmd_data == 'q':
           head.left(80)
           print("Turning head to the left!")
        elif cmd_data == 'e':
           head.right(80)
           print("Turning head to the right!")
        elif cmd_data == 'r':
           head.stop()
           print("Stopping head!")
        elif cmd_data == 'w':
          print("Moving forward!")
          motors.both(100)
        elif cmd_data == 's':
          print("Moving backward!")
          motors.both(-100)
        elif cmd_data == 'd':
          print("Turning right!")
          motors.left(100)
          motors.right(-100)
        elif cmd_data == 'a':
          print("Turning left!")
          motors.left(-100)
          motors.right(100)
        elif cmd_data == 'z':
          motors.stop()
        elif cmd_data == ' ':
          motors.stop()
          #reels.stop()
        elif cmd_data == 'p':
          sdata = sensors.poll(frequency=1, length=1, stream=stream_telemetry)
          print(sdata)
        elif cmd_data == 't':
          stream_telemetry = not stream_telemetry
          if stream_telemetry:
            print('Telemetry broadcast: ON')
          else:
            print('Telemetry broadcast: OFF')
  except (OSError, serial.SerialException):
    print('Serial connection error. Trying to reconnect...')
    connection.reconnect()
  except Exception as err:
    print("An error has ocurred")
    print(err)

  sys.stdout.flush()  # for service to print logs

terminate()

# vst.keeprunning = False
# vst.interrupt()
sur.keeprunning = False

# When everything done, release the capture
sock.close()
