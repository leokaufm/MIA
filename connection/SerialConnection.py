import platform
import time
import serial
import os
import termios

baudrate = 9600

TRIES = 3

system_platform = platform.system()
"""if system_platform == "Darwin":
  import FFMPegStreamer as pcs
  portname = '/dev/cu.usbmodem14101'
else:
  import H264Streamer as pcs
  portname = None """


class SerialConnection(object):
  def __init__(self):
    print("Connecting...")
    self.connect()

  def connect(self):
    self.open = False
    for t in range(0, TRIES):
      self.ser = self.serialcomm(timeout = 1)
      if self.ser is not None:
        self.open = True
        print('Opened port ' + str(self.ser))
        self.read(100000) # Cleanup
        print('Connected to bot Arduino module')
        return True

    print('Could not connect to Arduino module')
    return False

  def serialcomm(self, timeout):
    ser = None
    
    # Mac
    if system_platform == "Darwin":
      print('Mac environment. Trying port /dev/cu.usbmodem14101...')
      ser = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=baudrate, timeout=timeout)
    
    # Raspberry
    else:
      print('Raspi environment. Trying ports /dev/ttyACM...')
      for p in range(0, 5):
        port = '/dev/ttyACM' + str(p)
        if (os.path.exists(port)):
          ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
          break
        time.sleep(0.1)
    
    return ser

  def send(self, data):
    if self.ser is None:
      raise serial.SerialException('Serial connection not open')
    # print(f"Sending data {data.decode('utf-8')} to RPi")
    return self.ser.write(data)

  def read(self, length):
    if self.ser is None:
      raise serial.SerialException('Serial connection not open')
    return self.ser.read(length)

  # There could be a chance that whatever is behind the serial connection get stuck
  # and do not reply anything.  Hence I need a way to break this up (that is what trials is for)
  def readsomething(self, length):
    data = b''
    trials = 10000000

    while(len(data) < length and trials > 0):
      byte = self.ser.read(1)
      # print(byte)
      trials = trials - 1
      if (len(byte) > 0):
        data = b''.join([data, byte])

    return data

  def flush(self):
    """ if self.ser is not None:
      self.ser.flush()
      self.ser.flushInput()
      self.ser.flushOutput() """
    try:
        if self.ser and self.ser.is_open:
            self.ser.flush()
    except (serial.SerialException, termios.error) as e:
        print(f"[Flush Error] Could not flush serial port: {e}")
        self.reconnect()

  def close(self):
    if self.ser is not None:
      self.ser.close()

  def reconnect(self):
    try:
      self.flush()
      self.close()
    finally:
      self.connect()
    return self.open # True if succesfully reconnected
