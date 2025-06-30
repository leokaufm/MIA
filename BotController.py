# coding: latin-1
import socket
import sys
import time

from connection import MCast
import ConfigMe
import Configuration
from connection.H264Player import H264Player

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

video_streaming  = False

print('Press x to stop Bot')
print('Press i to start interaction sequence.')
print('Control the bot\'s movements with w, a, s, d (wheels), and q, e (head)')
print('Press ! to start video recording and streaming.')

while (True):
  time.sleep(0.3) # control here how long the bot does a movement
  print('>')
  data = None
  # Send h for hold to stop all motors
  while not data:
    sent = sock.sendto(bytes('U'+'h'+'000','ascii'), server_address)
    data = getch() 
  
  if (data.startswith('!')):
    if not video_streaming:
      print("Start video player, recording and streaming")
      # Configurations for video recording and streaming
      video_player = H264Player()
      video_player.spanAndConnect()
      sent = sock.sendto(bytes('S'+data+'000','ascii'), server_address)
      video_streaming = True
    else:
      print("Stop video player, recording and streaming")
      sent = sock.sendto(bytes('S'+data+'000','ascii'), server_address)
      video_player.interrupt()
      video_streaming = False
  elif (data.startswith('x')):
    break
  else:
    sent = sock.sendto(bytes('U'+data+'000','ascii'), server_address)
  
  

  

print("Stopping bot....")
for i in range(1, 100):
  sent = sock.sendto(bytes('U'+data+'000', 'ascii'), server_address)

sock.close()
