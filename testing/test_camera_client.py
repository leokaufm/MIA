#!/usr/bin/python3

import socket
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

# Camera setup
picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (1280, 720)})
picam2.configure(video_config)
encoder = H264Encoder(1000000)

# TCP socket setup
server_ip = "10.2.69.53"  # find out ip address of laptop (server) with hostname
server_port = 10001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))
stream = sock.makefile("wb")

# Combined outputs
output = FileOutput(stream)

# Start recording
picam2.start_recording(encoder, output)
time.sleep(20)
picam2.stop_recording()

# Clean up
stream.close()
sock.close()
