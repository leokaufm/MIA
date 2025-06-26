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
from connection.H264Streamer import H264Streamer
import Configuration

HOST = "10.2.69.133" # find out ip address on laptop (server) with "hostname -I"

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
  print('Stopping bot')
  try:
    # motors.stop()
    # reels.stop()
    os.remove('running.wt')
  finally:
    print('bot has stopped.')
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
print(f"myip: {myip}")

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

""" # Camera Streaming
system_platform = platform.system()
if system_platform == "Darwin": # Mac
  import FFMPegStreamer as pcs
else: # Windows, Linux
  import H264Streamer as pcs 

dosomestreaming = True

vst = pcs.H264VideoStreamer()
if (dosomestreaming):
  try:
    #vst.startAndConnect()
    vst.spanAndConnect()
    pass
  except Exception as e:
      print('Error starting H264 stream thread:'+str(e))"""

# Video Streaming
video_streaming = False

# Motors and Reels connections
connection = SerialConnection()
motors = SerialMotor(connection=connection)
head = SerialHead(connection=connection)

# Sensors - Telemetry
# sensors = TelemetryLoader(connection)


signal.signal(signal.SIGINT, lambda signum, frame: terminate())
signal.signal(signal.SIGTERM, lambda signum, frame: terminate())

# Control Loop
print('Bot ready to follow!')
# control_strategies = {
#   'follow_and_turn': control_functions.follow_turn,
#   'rotate_and_go': control_functions.rotate_go
# }
# control_strategy = control_strategies['follow_and_turn']

# stream_telemetry = True
# AUTONOMOUS_SLEEP = 0.05
# Live
while True:
  try:
    data = ''
    # TCP/IP server is configured as non-blocking
    sur.getmessage()

    cmd = sur.command
    cmd_data, address = sur.data, sur.address
    if cmd:
      print(f"cmd: {cmd}, cmd_data: {cmd_data}, address: {address}")

    if cmd == 'A':
      if (len(sur.message) == 5):
        # Sending the message that was received.
        print(sur.message)
        connection.send(sur.message)
        sur.message = ''
    
    elif cmd == "S":
      # Implement video streaming and recording
      if not video_streaming:
        # Set video streaming and recording
        video_streamer = H264Streamer(server_ip=HOST)
        print("Start video")
        video_streamer.spanAndConnect()
        video_streaming = True
      else:
        print("Stop video")
        video_streamer.interrupt()
        video_streaming = False      

    elif cmd == 'U':
      if cmd_data == 'x':
        motors.stop()
        head.stop()
        break
      elif cmd_data == 'h':
        motors.stop()
        head.stop()
        print("Bot on hold!")

      """ if cmd_data == 'M': # Enable/disable autonomous command
        autonomous = not autonomous
        reset_sensors()
        if autonomous:
          print('Auto mode: ON')
        else:
          print('Auto mode: OFF') """
      
      # Control strategies for autonomous mode
      """ elif cmd_data == '1':
        motors.stop()
        control_strategy = control_strategies['follow_and_turn']
        print('Control strat: Follow and Turn')
      elif cmd_data == '2':
        motors.stop()
        control_strategy = control_strategies['rotate_and_go']
        print('Control strat: Rotate and Go') """

      if cmd_data == '0':
        reset_sensors()
      
      else: # Manual commands
        if cmd_data == '':
          motors.stop()
          head.stop()
        elif cmd_data == 's': # backward
          motors.both(-80)
          # print(connection.read(1000))
        elif cmd_data == 'w': # forward
          motors.both(80)
          # print(f"Received msg: {connection.read(1000)}")
        elif cmd_data == 'd': # turn right
          motors.left(-80)
          motors.right(80)
        elif cmd_data == 'a': # turn left
          motors.left(80)
          motors.right(-80)
        elif cmd_data == 'z':
          motors.stop()
        elif cmd_data == 'q':
          head.left(40)
          time.sleep(0.2)
          head.stop()
        elif cmd_data == 'e':
          head.right(40)
          time.sleep(0.2)
          head.stop()
        elif cmd_data == 'r':
          head.stop()
        elif cmd_data == ' ':
          motors.stop()
          head.stop()
        elif cmd_data == 'i':
           motors.interaction()
        """ elif cmd_data == 't':
          stream_telemetry = not stream_telemetry
          if stream_telemetry:
            print('Telemetry broadcast: ON')
          else:
            print('Telemetry broadcast: OFF') """
  except (OSError, serial.SerialException):
    print('Serial connection error. Trying to reconnect...')
    connection.reconnect()
  except Exception as err:
    print("An error has ocurred")
    print(err)

  sys.stdout.flush()  # for service to print logs

terminate()

vst.keeprunning = False
vst.interrupt()
sur.keeprunning = False

# When everything done, release the capture
sock.close()
