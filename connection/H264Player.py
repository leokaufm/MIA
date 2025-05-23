import socket
import subprocess
import datetime
import os
import threading
import signal

PORT = 10001

class H264Player:
    def __init__(self):
        self.server_socket = None
        self.conn = None
        self.stream = None
        self.thread = None
        self.pro = None
    
    def spanAndConnect(self):
        try:
            FNULL = open(os.devnull, 'w')
            self.pro = subprocess.Popen(['/usr/bin/python3', 'connection/H264Player.py'],preexec_fn=os.setsid)
            if self.pro.stderr or self.pro.returncode:
                return False
        except Exception as e:
            print ("Error:" + str(e))
            print ("Error: unable to start a new thread")

    def startAndConnect(self):
        try:
            self.thread = threading.Thread(target=self.streamAndRecordVideo, args=(1,))
            self.thread.start()
        except Exception as e:
            print ("Error:" + str(e))
            print ("Error: unable to start a new thread") 

    def streamAndRecordVideo(self, name):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", PORT))
        self.server_socket.listen(1)
        print(f"Listening on TCP port {PORT}...")
        self.conn, addr = self.server_socket.accept()
        print(f"Connection from {addr}")
        self.stream = self.conn.makefile("rb")
        # Opens window for video streaming
        """ ffplay = subprocess.Popen(
            ["ffplay", "-fflags", "nobuffer", "-framedrop", "-"],
            stdin=subprocess.PIPE
        ) """

        t = datetime.datetime.now()
        output_file = "mia_" + t.strftime("%Y-%m-%d_%H-%M-%S") + ".h264"
        with open(output_file, "wb") as f:
            try:
                while True:
                    data = self.stream.read(4096)
                    if not data:
                        break
                    f.write(data)
                    # ffplay.stdin.write(data)
            except KeyboardInterrupt:
                print("\nStopped.")
            finally:
                self.stream.close()
                # ffplay.stdin.close()
                # ffplay.wait()
                self.conn.close()
                self.server_socket.close()
                print("Video saved to", output_file)

    def interrupt(self):
        print ('Interrupting stream h264 streamer...')

        if (self.pro):
            os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)  
            print('Killing process')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ("0.0.0.0", PORT)
            sock.connect(server_address)
            sock.send(b'1')
            sock.close()
        except Exception as e:
            print('Streaming Server seems to be down:' + str(e))

if __name__ == "__main__":
    vd = H264Player()
    vd.startAndConnect()

    input()