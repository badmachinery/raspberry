import serial
import logging


class Arduino:
    def __init__(self, _address, do_connect=False):
        self.address = _address
        self.connection = None
        self.connected = False
        if do_connect:
            self.connect()

    def close(self):
        logging.info("Arduino '{0}' :: Closing connection to {0}".format(self.address))
        self.connection.close()
        self.connected = False
        logging.info("Arduino '{0}' :: Connection to {0} closed".format(self.address))

    def connect(self):
        logging.info("Arduino '{0}' :: Connecting to {0}".format(self.address))
        try:
            self.connection = serial.Serial(self.address, timeout=0.001, baudrate=115200)
            self.connected = True
            logging.info("Arduino '{0}' :: Successfully connected to {0}".format(self.address))
            return True
        except Exception:
            logging.critical("Arduino '{0}' :: Connection failed".format(self.address))
            quit()

    def reconnect(self):
        self.close()
        self.connect()

    def is_connected(self):
        return self.connected

    def send(self, symbol, data):
        try:
            if self.is_connected():
                self.connection.write((symbol + str(data) + '\n').encode('ascii'))
        except Exception:
            logging.warning("Arduino '{}' :: Sending exception ({}{})".format(self.address, symbol, data))

    def send_raw(self, data):
        try:
            if self.is_connected():
                self.connection.write(str(data).encode('ascii'))
        except Exception:
            logging.warning("Arduino '{}' :: Sending exception ({})".format(self.address, data))

    def receive(self, size=1024):
        try:
            if self.is_connected():
                return self.connection.read(size)
            else:
                return None
        except Exception:
            logging.warning("Arduino '{}' :: Receiving exception".format(self.address))
