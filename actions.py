import time
import re
import smbus
from random import randint

from threads import thread_handler
from arduino_lib import arduino_sensors, arduino_engine
from connection import socket_server
import constants as c
import vars as v
import scripts

def arduino_read_cycle():
    '''
    1) Update current time
    2) Check shutdown signal
    3) Reading sensors data: updating variables at vars.py
    4) Reading engine data
    5) Reconnecting if necessary
    '''
    while True:
        ''' 1) '''
        v.current_time_sensors = time.time()

        ''' 2) '''
        if thread_handler.events['arduino_read_cycle'].is_set():
            return True

        ''' 3) '''
        read_ultrasonic_sensors()
        ''' 4) '''
        read_arduino_engine()

        ''' 5) '''
        #if abs(v.current_time_sensors - v.arduino_engine_last_answer) > c.RECONNECTION_TIME:
        #    arduino_engine.conneced = False
        #    print('Reconnecting arduino_engine')
        #    arduino_engine.reconnect()
        #    v.arduino_engine_last_answer = time.time()

        #if (v.current_time_sensors - v.arduino_sensors_last_answer > c.RECONNECTION_TIME):
        #    print('Reconnecting arduino_sensors')
        #    arduino_sensors.reconnect()
        #    v.arduino_sensors_last_answer = time.time()

def client_read_cycle():
    '''
    1) Update current time
    2) Check shutdown signal
    3) Receiving data from client
    4) Trying to read command from client
    5) Trying to read data from client
    6) Shutting down if connection lost
    '''
    while True:
        ''' 1) '''
        v.current_time_client = time.time()

        ''' 2) '''
        if thread_handler.events['client_read_cycle'].is_set():
            return True

        ''' 3) '''
        data = socket_server.receive()
        if data:
            data = data.decode('ascii')
            v.client_last_answer = time.time()
            ''' 4) '''
            command = re.search(r'C.+?\n', data)
            if command:
                command = re.sub(r'C|\n', '', command.group(0))
                v.client_commands.append(command)
            ''' 5) '''
            speed = re.search(r's.+?\n', data)
            if speed:
                speed = re.sub(r's|\n', '', speed.group(0))
                if speed:
                    speed = int(speed)
                v.engine_speed = speed
            rotation = re.search(r'r.+?\n', data)
            if rotation:
                rotation = re.sub(r'r|\n', '', rotation.group(0))
                if rotation:
                    rotation = int(rotation)
                v.rotation_angle = rotation

        ''' 6) '''
        #if v.current_time_client - v.client_last_answer < c.LOST_CONNECTION_TIME:
        #    thread_handler.stop_all_threads()
        #    v.state = c.STATE_LOST

def main_cycle():
    '''
    1) Check shutdown signal
    2) Executing commands
    3) Check obstacles to evade
    4) Sending data to arduino if we are in manual state
    5) Printing data if we want to
    '''
    while True:
        ''' 1) '''
        if thread_handler.events['main_cycle'].is_set():
            thread_handler.stop_all_threads()
            time.sleep(0.2)
            arduino_engine.close()
            arduino_sensors.close()
            socket_server.close()
            return True

        ''' 2) '''
        commands = v.client_commands.copy()
        v.client_commands.clear()
        for command in commands:
            try:
                command_handler[command]()
            except KeyError:
                print ("Unknown command: '{}'".format(command))

        ''' 3) '''
        if scripts.obstacle_is_at_front():
            pass
            #v.state = c.STATE_BACK
            #thread_handler.new_thread(scripts.simple_front_obstacle_evasion(v.state))

        ''' 4) '''
        if v.state == c.STATE_MANUAL:
            send_data_to_arduino_engine()

        ''' 5) '''
        #print (v.obstacle_distance_front_left, v.obstacle_distance_front_right, v.obstacle_distance_left, v.obstacle_distance_right)
        #print(v.engine_speed, v.rotation_angle)

def read_ultrasonic_sensors():
    data = arduino_sensors.receive(70)
    if data:
        v.arduino_sensors_last_answer = time.time()
        data = data.decode('ascii')
        if data[0] == 'D':
            help = re.findall(r'd', data)
            if len(help) == 3:
                match = re.findall(r'\d+', data)
                if match:
                    match = list(map(int, match))
                    if len(match) == 4:
                        v.obstacle_distance_front_left = match[0]
                        v.obstacle_distance_front_right = match[1]
                        v.obstacle_distance_left = match[2]
                        v.obstacle_distance_right = match[3]

def read_arduino_engine():
    data = arduino_engine.receive(32)
    if data:
        v.arduino_engine_last_answer = time.time()

def send_data_to_arduino_engine(speed=None, rotation=None):
    if speed:
        arduino_engine.send('s', speed)
    else:
        arduino_engine.send('s', v.engine_speed)
    if rotation:
        arduino_engine.send('r', rotation)
    else:
        arduino_engine.send('r', v.rotation_angle)

def handle_command_stop():
    thread_handler.stop_all_threads()

def handle_command_script():
    v.state = c.STATE_AUTO
    thread_handler.new_thread(scripts.custom_script)

def handle_command_reload():
    print('Reconnecting')
    arduino_engine.reconnect()
    #arduino_sensors.reconnect()

def handle_command_way():
    thread_handler.new_thread(scripts.move_through_the_corridor, name='move_through_the_corridor')

def handle_command_break():
    scripts.do_break()

command_handler = {
'Stop': handle_command_stop,
'Auto': handle_command_script,
'Load': handle_command_reload,
'Way': handle_command_way,
'Break': handle_command_break
}
