import serial

class Arduino:
    def __init__(self, _address, do_connect=False):
        self.address = _address
        if do_connect:
            self.connect()

    def close(self):
        self.connection.close()
        self.connected = False

    def connect(self):
        print('Connecting to /dev/tty/ACM' + str(self.address))
        try:
            self.connection = serial.Serial('/dev/ttyACM' + str(self.address), timeout=0.001, baudrate=115200)
            self.connected = True
        except Exception:
            print('Connection failed. Exiting')
            quit()
        print('Connectoin succeed')

    def reconnect(self):
        self.close()
        self.connect()

    def is_connected(self):
        return self.connected

    def send(self, symbol, data):
        self.connection.write((symbol + str(data) + '\n').encode('ascii'))

    def send_raw(self, data):
        ''' data - str '''
        self.connection.write(data.encode('ascii'))

    def receive(self, size=1024):
        return self.connection.read(size)

arduino_sensors = Arduino(1)
arduino_engine = Arduino(0)
