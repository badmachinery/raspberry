import socket
import serial

class Arduino:
    def __init__(self):
        try:
            self.connection = serial.Serial("/dev/ttyACM0", timeout=0.001)
            self.is_connected = True
        except Exception:
            self.connection = serial.Serial("/dev/ttyACM1", timeout=0.001)
            self.is_connected = True

    def send_data(self, *data):
        data_block = b''
        for s in data:
            data_block += str(s).encode('ascii') + '/'.encode('ascii')
        self.connection.write(data_block)

    def receive_data(self):
        received = self.connection.read(32)
        received = received.decode('ascii')
        return received

class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.sock.listen(1)

        print('Waiting for connection..')
        self.connection, self.address = self.sock.accept()

        self.arduino = Arduino()
        while(1):
            data = self.connection.recv(1024)
            if (data):
                self.arduino.connection.write(data)

def main():
    server = Server()

if __name__ == "__main__":
    main()
