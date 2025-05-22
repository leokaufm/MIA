import socket
import time
import os
import subprocess
import threading
import signal
from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

HOST = "10.2.69.53" # find out ip address on laptop (server) with "hostname -I"

class H264Streamer:
    def __init__(self, server_ip):
        self.picam2 = None
        self.encoder = None
        self.server_ip = server_ip
        self.player_port = 10001
        self.stream = None
        self.output = None
        self.client_socket = None
        self.thread = None

        self.running = True

    def spanAndConnect(self):
        try:
            FNULL = open(os.devnull, 'w')
            self.pro = subprocess.Popen(['/usr/bin/python3', 'connection/H264Streamer.py'],preexec_fn=os.setsid)
            if self.pro.stderr or self.pro.returncode:
                return False
        except Exception as e:
            print ("Error:" + str(e))
            print ("Error: unable to start a new thread")

    def startAndConnect(self):
        try:
            self.thread = threading.Thread(target=self.startVideo, args=(1,))
            self.thread.start()
        except Exception as e:
            print ("Error:" + str(e))
            print ("Error: unable to start a new thread")

    def startVideo(self, name):
       """ print("Sleep 5")
       time.sleep(5)
       print("Woke up") """
       # Picam2 setup
       self.picam2 = Picamera2()
       self.encoder = H264Encoder(1000000)
       video_config = self.picam2.create_video_configuration({"size": (1280, 720)}, transform=Transform(vflip=1, hflip=1))
       self.picam2.configure(video_config)

       # TCP socket setup
       self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.client_socket.connect((self.server_ip, self.player_port))

       # Prepare file format
       self.stream = self.client_socket.makefile("wb")
       self.output = FileOutput(self.stream)

       # Start recording
       self.picam2.start_recording(self.encoder, self.output)
       print("Recording started")
    
    def interrupt(self):
        print ('Interrupting stream h264 streamer...')

        if (self.pro):
            os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)  
            print('Killing process')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.server_ip, self.player_port)
            sock.connect(server_address)
            sock.send(b'1')
            sock.close()
        except Exception as e:
            print('Streaming Server seems to be down:' + str(e))

if __name__ == "__main__":
    vd = H264Streamer(server_ip = HOST)
    vd.startAndConnect()

    input()
