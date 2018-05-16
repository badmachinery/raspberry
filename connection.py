import socket

class Socket_server:
    def __init__(self, do_create=False):
        if do_create:
            self.create()

    def create(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9091))
        self.sock.listen(1)
        print('Waiting for connection from client')
        self.connection, self.address = self.sock.accept()
        print('Client succesfully connected')

    def close(self):
        self.connection.close()

    def recreate(self):
        self.close()
        self.create()

    def send(self, symbol, data):
        self.connection.send((symbol + str(data) + '\n').encode('ascii'))

    def send_raw(self, data):
        self.connection.send((str(data) + '\n').encode('ascii'))

    def receive(self, size=32):
        return self.connection.recv(size)

socket_server = Socket_server()
