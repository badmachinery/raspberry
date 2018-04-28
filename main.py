import threading
import time

import connection
import arduino

def manual_write_cycle(server, ard):
        while(1):
            data = server.receive()
            if data and ard.is_connected():
                if (len(data) == 6):
                    ard.send(data)
                else:
                    ard.send(data[0:6])

def read_cycle(server, ard):
        resetter = time.clock()
        while(1):
            if (time.clock() - resetter > 0.2):
                ard.reconnect()
                resetter = time.clock()

            data = ard.receive(32)
            if data:
                resetter = time.clock()

def main():
    server = connection.Socket_server(do_create=True)
    ard = arduino.Arduino(do_connect=True)

    thread1 = threading.Thread(target=manual_write_cycle, args=(server, ard))
    thread2 = threading.Thread(target=read_cycle, args=(server, ard))
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()
