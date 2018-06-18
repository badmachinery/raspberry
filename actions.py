import time
import re
import logging

import consts
import vars
import scripts
from utility import log


#@log
def arduino_read():
    vars.arduino.send('u', 0)

    data = vars.arduino.receive(1024)
    if data:
        vars.arduino_data += data.decode('ascii')
        vars.arduino_last_update = time.time()
    #else:
    #    print('Resetting')
    #    logging.debug('Resetting arduino')
    #    vars.arduino.reconnect()
    #    scripts.stop()
    #    vars.state = consts.state['manual']

    while True:
        index = vars.arduino_data.find('\n')
        if index == -1:
            break

        data = vars.arduino_data[:index]
        vars.arduino_data = vars.arduino_data[index + 1:]

        if data[0] in consts.command_group['sensors']:
            update_sensor_data(data)


#@log
def client_messaging():
    read_client()
    send_ultrasonic_data()

#@log
def main_cycle():
    vars.server.create()
    vars.arduino.connect()

    vars.client_last_update = time.time()
    vars.arduino_last_update = time.time()

    while True:
        logging.debug('main_cycle :: start iteration')
        client_messaging()  # We execute commands there, remember that
        arduino_read()
        state_to_actions[vars.state]()
        logging.debug('main_cycle :: end iteration')


def update_sensor_data(data):
    nums = int(data[1:])
    if data[0] == consts.command_symbol_arduino['sensor_forward']:
        vars.sensor_front_data = nums
        logging.debug('sensor_front_data -> {}'.format(nums))
    elif data[0] == consts.command_symbol_arduino['sensor_left']:
        vars.sensor_left_data = nums
        logging.debug('sensor_left_data -> {}'.format(nums))
    elif data[0] == consts.command_symbol_arduino['sensor_right']:
        vars.sensor_right_data = nums
        logging.debug('sensor_right_data -> {}'.format(nums))


#@log
def send_data_to_arduino(speed=None, rotation=None):
    if not speed:
        speed = vars.engine_speed
    if not rotation:
        rotation = vars.rotation

    vars.arduino.send('s', speed)
    vars.arduino.send('r', rotation)

    logging.debug("Speed: {}, Rotation: {}".format(speed, rotation))


#@log
def read_client():
    data = vars.server.receive(1024)
    if data:
        logging.debug('Data: {}'.format(data))
        vars.socket_data += data.decode('ascii')
        vars.client_last_update = time.time()

    if time.time() - vars.client_last_update > consts.lost_connection_time:
        logging.debug('Connection lag')
        scripts.stop()
        vars.state = consts.state['manual']
        vars.socket_data = ''

    while True:
        index = vars.socket_data.find('\n')
        if index == -1:
            break

        data = vars.socket_data[:index]
        vars.socket_data = vars.socket_data[index + 1 :]

        if data[0] in consts.command_group['client']:
            execute_command(data)

#@log
def execute_command(command):
    if command in consts.command_group['manual']:
        if vars.state == consts.state['manual']:
            execute_manual_command(command)
    else:
        try:
            vars.state = command_to_state[command]
        except KeyError:
            logging.warning("Unknown command: '{}'".format(command))


def execute_manual_command(command):
    if command == consts.command_symbol_client['forward']:
        vars.engine_speed = consts.engine_speed[vars.engine_speed_max]
    elif command == consts.command_symbol_client['backward']:
        vars.engine_speed = consts.engine_speed[-vars.engine_speed_max]
    elif command == consts.command_symbol_client['stay']:
        vars.engine_speed = consts.engine_speed[0]
    elif command == consts.command_symbol_client['speed_up']:
        vars.engine_speed_max += 1
        if vars.engine_speed_max == 4:
            vars.engine_speed_max = 3
    elif command == consts.command_symbol_client['speed_down']:
        vars.engine_speed_max -= 1
        if vars.engine_speed_max == 0:
            vars.engine_speed_max = 1
    elif command == consts.command_symbol_client['left']:
        if vars.engine_speed == consts.engine_speed[0]:
            vars.rotation = consts.rotation[-3]
        else:
            vars.rotation = consts.rotation[-1]
    elif command == consts.command_symbol_client['right']:
        if vars.engine_speed == consts.engine_speed[0]:
            vars.rotation = consts.rotation[3]
        else:
            vars.rotation = consts.rotation[1]
    elif command == consts.command_symbol_client['middle']:
        vars.rotation = consts.rotation[0]


#@log
def send_ultrasonic_data():
    vars.server.send('Q', vars.sensor_front_data)
    vars.server.send('L', vars.sensor_left_data)
    vars.server.send('R', vars.sensor_right_data)


#@log
def actions_state_manual():
    if scripts.obstacle_is_at_front():
        scripts.stop()
        logging.debug("Obstacle is at front -> breaking")
    send_data_to_arduino()


#@log
def actions_state_exit():
    scripts.stop()
    vars.arduino.close()
    vars.server.close()
    quit(0)


#@log
def actions_state_reload():
    vars.arduino.reconnect()
    print('Reconnect')
    vars.state = consts.state['manual']
    logging.debug("State changed :: STATE_MANUAL")


#@log
def actions_state_way():
    '''
    res = scripts.move_through_the_corridor()
    if res == True:
        vars.state = consts.state['manual']
        logging.debug("State changed :: STATE_MANUAL")
        print('Done')
    '''
    vars.arduino.send('w', 0)
    print('WAY')
    time.sleep(0.1)
    vars.state = consts.state['manual']

def actions_state_idle():
    pass


command_to_state = {
    consts.command_symbol_client['exit']: consts.state['exit'],
    consts.command_symbol_client['reload']: consts.state['reload'],
    consts.command_symbol_client['way']: consts.state['way'],
    consts.command_symbol_client['idle']: consts.state['idle'],
}

state_to_actions = {
    consts.state['manual']: actions_state_manual,
    consts.state['exit']: actions_state_exit,
    consts.state['reload']: actions_state_reload,
    consts.state['way']: actions_state_way,
    consts.state['idle']: actions_state_idle,
}
