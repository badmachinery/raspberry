import socket
import serial
import threading
import time

class Arduino:
    def __init__(self):
        self.connect()

    def close(self):
        self.connection.close()
        self.connected = False

    def connect(self):
        try:
            self.connection = serial.Serial("/dev/ttyACM0", timeout=0.001, write_timeout=0.001, baudrate=115200)
            #self.connection = serial.Serial("/dev/ttyACM0", baudrate=115200)
            self.connected = True
        except Exception:
            self.connection = serial.Serial("/dev/ttyACM1", timeout=0.001, write_timeout=0.001, baudrate=115200)
            #self.connection = serial.Serial("/dev/ttyACM1", baudrate=115200)
            self.connected = True

    def reconnect(self):
        self.close()
        self.connect()

    def is_connected(self):
        return self.connected

    def send_data(self, *data):
        data_block = b''
        for s in data:
            data_block += str(s).encode('ascii') + '/'.encode('ascii')
        self.connection.write(data_block)

    def receive_data(self):
        received = self.connection.read(32)
        #received = received.decode('ascii')
        return received

class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.sock.listen(1)

        print('Waiting for connection..')
        self.connection, self.address = self.sock.accept()
        print('Connected')

        self.arduino = Arduino()

        thread1 = threading.Thread(target=self.manual_write_cycle)
        thread2 = threading.Thread(target=self.read_cycle)
        thread1.start()
        thread2.start()

    def manual_write_cycle(self):
        while(1):
            data = self.connection.recv(1024)
            if data and self.arduino.is_connected():
                if (len(data) == 6):
                    self.arduino.connection.write(data)
                else:
                    self.arduino.connection.write(data[0:6])

    def read_cycle(self):
        resetter = time.clock()
        while(1):
            if (time.clock() - resetter > 0.1):
                print('Reset')
                self.arduino.reconnect()
                resetter = time.clock()

            data = self.arduino.receive_data()
            if data:
                resetter = time.clock()

def main():
    server = Server()

if __name__ == "__main__":
    main()
