# coding: latin-1
import socket
import sys
import time

from connection import MCast
import ConfigMe
import Configuration
from connection.H264Server import H264Server

# Socket for transmitting commands to the bot
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Fetch the remote ip if I do not have one.  It should be multicasted by ShinkeyBot
reporter = MCast.Receiver()

ConfigMe.createconfig("config.ini")

# Load the configuration file
lastip = ConfigMe.readconfig("config.ini")

print("Last ip used:"+lastip)

if (len(sys.argv)<2):
    print ("Waiting for Multicast Message")
    botip = reporter.receive()
    print ('Bot IP:' + botip)
    ip = botip
elif sys.argv[1] == '-f':
    print ("Forcing IP Address")
    ip = lastip
else:
    ip = sys.argv[1]
    print ("Using IP:"+ip)

ConfigMe.setconfig("config.ini","ip",ip)
server_address = (ip, Configuration.controlport)

def _find_getch():
  try:
    import termios
  except ImportError:
    # Non-POSIX. Return msvcrt's (Windows') getch.
    import msvcrt
    return msvcrt.getch

  # POSIX system. Create and return a getch that manipulates the tty.
  import tty

  def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

  return _getch


getch = _find_getch()

print('Press x to stop Bot')
print('Press f to enter new update frequency for the bot.')
print('Press i to start interaction sequence.')
print('Press ! to start video recording and streaming.')

while (True):
  time.sleep(0.1) # control here how long the bot does a movement
  print('>')
  data = None
  # Send h for hold to stop all motors
  while not data:
    sent = sock.sendto(bytes('U'+'h'+'000','ascii'), server_address)
    data = getch()
  
  if (data.startswith('f')): # ???
    newfreq = input('Freq:');
    sent = sock.sendto(bytes('AE'+'{:3d}'.format(newfreq),'ascii'), server_address)
    sent = sock.sendto(bytes('AB'+'{:3d}'.format(1),'ascii'), server_address)
    """ elif (data.startswith('c')):
        print('Command:')
        cmd = sys.stdin.readline()
        sent = sock.sendto(bytes(cmd,'ascii'), server_address) """
  elif (data.startswith('!')):
    print("Start video recording and streaming")
    # Configurations for video recording and streaming
    video_server = H264Server()
    # video_server.connect()
    video_server.spanAndConnect()
    sent = sock.sendto(bytes('S'+data+'000','ascii'), server_address)
    """ elif (data.startswith('?')):
      print("Stop video recording and streaming") 
      sent = sock.sendto(bytes('S'+data+'000','ascii'), server_address)"""
  elif (data.startswith('x')):
    break
  else:
    sent = sock.sendto(bytes('U'+data+'000','ascii'), server_address)
  
  """elif (data.startswith('i')):
      sent = sock.sendto(bytes(cmd,'ascii'), server_address)"""

  

print("Stopping ALPIBot....")
for i in range(1, 100):
  sent = sock.sendto(bytes('U'+data+'000', 'ascii'), server_address)

sock.close()
