import actions
from threads import thread_handler
from connection import socket_server
from arduino_lib import arduino_sensors, arduino_engine

def main():
    socket_server.create()
    arduino_sensors.connect()
    arduino_engine.connect()

    thread_handler.new_thread(function=actions.client_read_cycle, name='client_read_cycle')
    thread_handler.new_thread(function=actions.arduino_read_cycle, name='arduino_read_cycle')
    thread_handler.new_thread(function=actions.main_cycle, name='main_cycle')

if __name__ == "__main__":
    main()
