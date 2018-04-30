import time
import re
import smbus
from random import randint

from threads import thread_handler
from arduino_lib import arduino
from connection import socket_server
import constants as c

bus = smbus.SMBus(1)
address = 0x4

def i2c_send(data):
    for i in data:
        bus.write_byte(address, i)

def arduino_reader():
    print('Arduino reader')
    last_message_time = time.clock()
    while True:
        if thread_handler.events['arduino_reader'].is_set():
            return True

        if (time.clock() - last_message_time > 0.6): #This value seems OK
            print('Reset')
            arduino.reconnect()
            last_message_time = time.clock()

        if arduino.is_connected():
            data = arduino.receive(32)
            if data:
                last_message_time = time.clock()

def client_reader():
    print('Client reader')
    state = c.MANUAL_STATE
    while True:
        if thread_handler.events['client_reader'].is_set():
            return True

        data = socket_server.receive()
        if data:
            command = re.search(r'R.+?\n', data.decode('ascii'))
            if command:
                command = re.sub(r'R|\n', '', command.group(0))
                if command == 'stop':
                    thread_handler.stop_all_threads()
                    time.sleep(0.2)
                    arduino.close()
                    socket_server.close()
                    return True
                elif command == 'script':
                    thread_handler.new_thread(custom_script)
                    c.state = c.AUTO_STATE
                elif command == 'reload':
                    arduino.reconnect()
            else:
                if c.state == c.MANUAL_STATE:
                    #i2c_send(data)
                    if arduino.is_connected():
                        arduino.send(data)

def move(speed, rotation, seconds):
    t = time.time()
    while time.time() - t < seconds:
        arduino.send(('s' + str(speed) + '\n').encode('ascii'))
        arduino.send(('r' + str(rotation) + '\n').encode('ascii'))

def custom_script():
    move(7400, 7200, 3)
    move(7400, 7600, 5)
    move(6800,6800, 2)
    move(7400, 7200, 2)

    #for i in range(5):
    #    move(randint(7200, 7500), randint(7200, 7500), 2)

    c.state = c.MANUAL_STATE
