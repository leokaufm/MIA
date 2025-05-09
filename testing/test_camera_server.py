# server_tcp_receiver.py

import socket
import subprocess

PORT = 10001
OUTPUT_FILE = "received.h264"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(1)
print(f"Listening on TCP port {PORT}...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")
stream = conn.makefile("rb")

ffplay = subprocess.Popen(
    ["ffplay", "-fflags", "nobuffer", "-framedrop", "-"],
    stdin=subprocess.PIPE
)

with open(OUTPUT_FILE, "wb") as f:
    try:
        while True:
            data = stream.read(4096)
            if not data:
                break
            f.write(data)
            ffplay.stdin.write(data)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        stream.close()
        ffplay.stdin.close()
        ffplay.wait()
        conn.close()
        server_socket.close()
        print("Video saved to", OUTPUT_FILE)
