class SerialHead:
  def __init__(self, *, connection):
    self.connection = connection

  def left(self, speed):
    self.connection.send(bytes('A0A'+'{:3d}'.format(speed), 'ascii'))

  def right(self, speed):
    self.connection.send(bytes('A0B'+'{:3d}'.format(speed), 'ascii'))

  def stop(self):
    self.connection.send(bytes('A0C000', 'ascii'))