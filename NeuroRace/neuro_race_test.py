import socket

# Blue robot: 192.168.0.101
# Red robot: 192.168.0.100
UDP_IP = "192.168.0.101"  # Replace with ESP8266 IP
UDP_PORT = 4210
MESSAGE = "0"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
