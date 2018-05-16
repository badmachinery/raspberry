import socket
import logging

class SocketServer:
    def __init__(self, do_create=False):
        if do_create:
            self.create()

    def create(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9091))
        self.sock.listen(1)
        logging.info('Server :: Waiting for connection')
        self.connection, self.address = self.sock.accept()
        logging.info("Server :: Accepted connection on address '{}'".format(self.address))

    def close(self):
        self.connection.close()
        logging.info("Server :: Closing connection on address '{}'".format(self.address))

    def recreate(self):
        self.close()
        self.create()

    def send(self, symbol, data):
        self.connection.send((symbol + str(data) + '\n').encode('ascii'))

    def send_raw(self, data):
        self.connection.send((str(data) + '\n').encode('ascii'))

    def receive(self, size=32):
        return self.connection.recv(size)


