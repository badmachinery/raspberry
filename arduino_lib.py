import serial

class Arduino:
    def __init__(self, do_connect=False):
        if do_connect:
            self.connect()

    def close(self):
        self.connection.close()
        self.connected = False

    def connect(self):
        print('Arduino connecting')
        try:
            self.connection = serial.Serial("/dev/ttyACM0", timeout=0.001, baudrate=115200)
            self.connected = True
        except Exception:
            self.connection = serial.Serial("/dev/ttyACM1", timeout=0.001, baudrate=115200)
            self.connected = True
        print('Connected')

    def reconnect(self):
        self.close()
        self.connect()

    def is_connected(self):
        return self.connected

    def send(self, data):
        self.connection.write(data)

    def receive(self, size=1024):
        return self.connection.read(size)

arduino = Arduino()
