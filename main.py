import actions
from threads import thread_handler
from connection import socket_server
from arduino_lib import arduino

def main():
    socket_server.create()
    arduino.connect()

    thread_handler.new_thread(function=actions.client_reader, name='client_reader')
    thread_handler.new_thread(function=actions.arduino_reader, name='arduino_reader')

if __name__ == "__main__":
    main()
