import time
import re
import smbus
from random import randint

from threads import thread_handler
from arduino_lib import arduino1, arduino2
from connection import socket_server
import constants as c

qwall = 100
ewall = 100
lwall = 100
rwall = 100

def arduino_reader():
    global qwall, rwall, ewall, lwall

    print('Arduino reader')
    last_message_time = time.clock()
    while True:
        if thread_handler.events['arduino_reader'].is_set():
            return True

        #if (time.clock() - last_message_time > 0.6): #This value seems OK
        #    print('Reset')
        #    arduino.reconnect()
        #    last_message_time = time.clock()

        if arduino1.is_connected():
            data = arduino1.receive(32)
            if data:
                last_message_time = time.clock()
                data = data.decode('ascii')
                if data[0] == 'Q':
                    match = re.search(r'[^QELR]\d+[^\n]', data)
                    if match:
                        qwall = int(match.group(0))
                elif data[0] == 'E':
                    match = re.search(r'[^QELR]\d+[^\n]', data)
                    if match:
                        ewall = int(match.group(0))
                elif data[0] == 'L':
                    match = re.search(r'[^QELR]\d+[^\n]', data)
                    if match:
                        lwall = int(match.group(0))
                elif data[0] == 'R':
                    match = re.search(r'[^QELR]\d+[^\n]', data)
                    if match:
                        rwall = int(match.group(0))
                if (0 < ewall < 30 or 0 < qwall < 30) and (c.mode != c.MODE_BACK):
                    c.mode = c.MODE_BACK
                    print('Evasion')
                    print('Qwall: {}, Ewall: {}, Rwall: {}, LWall: {}'.format(qwall, ewall, rwall, lwall))
                    thread_handler.new_thread(test)

        if arduino2.is_connected():
            data = arduino2.receive(32)
            if data:
                last_message_time = time.clock()

def client_reader():
    print('Client reader')
    c.mode = c.MODE_MANUAL

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
                    arduino1.close()
                    arduino2.close()
                    socket_server.close()
                    return True
                elif command == 'script':
                    thread_handler.new_thread(custom_script)
                    c.state = c.MODE_AUTO
                elif command == 'reload':
                    arduino1.reconnect()
                    arduino2.reconnect()
            else:
                if c.mode == c.MODE_MANUAL:
                    if arduino2.is_connected():
                        arduino2.send(data)

def move(speed, rotation, seconds):
    t = time.time()
    while time.time() - t < seconds:
        arduino2.send(('s' + str(speed) + '\n').encode('ascii'))
        arduino2.send(('r' + str(rotation) + '\n').encode('ascii'))

def custom_script():
    for i in range(5):
        move(c.ENGINE_SPEED[randint(-1, 1)], randint(6000, 8000), 2)
    c.mode = c.MODE_MANUAL

def test():
    move(c.ENGINE_SPEED[0], c.SERVO_ANGLE[0], 0.1)
    move(c.ENGINE_SPEED[-1], c.SERVO_ANGLE[0], 0.5)
    print('Evaded')
    c.mode = c.MODE_MANUAL
