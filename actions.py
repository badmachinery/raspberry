import time
import re
import logging

import consts
import vars
import scripts


def arduino_read():
    logging.debug('@ arduino_read')
    # current_time = time.time()    # Update current time
    #read_ultrasonic_sensors()
    read_arduino_engine()
    '''
    if abs(current_time - vars.arduino_engine_last_answer_time) > consts.RECONNECTION_TIME:    # Reconnecting engine
        arduino_engine.connected = False
        print('Reconnecting arduino_engine')
        arduino_engine.reconnect()
        vars.arduino_engine_last_answer = time.time()
    
    if (vars.current_time_sensors - vars.arduino_sensors_last_answer > consts.RECONNECTION_TIME):    # Reconnecting sensors
        print('Reconnecting arduino_sensors')
        arduino_sensors.reconnect()
        vars.arduino_sensors_last_answer = time.time()
    '''
    logging.debug('$ arduino_read')


def client_messaging():
    logging.debug('@ client_messaging')
    # current_time = time.time() # Update current time
    read_client()
    '''
    if vars.current_time_client - vars.client_last_answer < consts.LOST_CONNECTION_TIME:   # Shutdown if connections lost
        thread_handler.stop_all_threads()
        vars.state = consts.STATE_LOST
    '''
    send_ultrasonic_data()
    logging.debug('$ client_messaging')


def main_cycle():
    logging.debug('@ main_cycle')
    vars.server.create()
    vars.arduino_engine.connect()
    #vars.arduino_sensors.connect()

    while True:
        logging.debug('main_cycle :: start iteration')
        client_messaging()  # We execute commands there, remember that
        arduino_read()
        state_to_actions[vars.state]()
        logging.debug('main_cycle :: end iteration')
    #Max - 0.045 seconds

def read_ultrasonic_sensors():
    logging.debug('@ read_ultrasonic_sensors')
    data = vars.arduino_sensors.receive(70)
    if data:
        # vars.arduino_sensors_last_answer_time = time.time()
        data = data.decode('ascii')
        logging.debug("Data: {}".format(data))
        if data[0] == 'D':
            temp = re.findall(r'd', data)
            if len(temp) == 2:
                match = re.findall(r'\d+', data)
                if match:
                    match = list(map(int, match))
                    if len(match) == 3:
                        if 1 < match[0] < 50:
                            scripts.do_break()

                        vars.obstacle_distance_front_left = match[0]
                        vars.obstacle_distance_left = match[1]
                        vars.obstacle_distance_right = match[2]
                        logging.debug('Ultrasonic values changed to: {}, {}, {}'.format(match[0], match[1],
                                                                                            match[2]))
    logging.debug('$ read_ultrasonic_sensors')


def read_arduino_engine():
    logging.debug('@ read_arduino_engine')
    data = vars.arduino_engine.receive(32)
    if data:
        print (data)
    # if data:
    #     vars.arduino_engine_last_answer_time = time.time()
    logging.debug('$ read_arduino_engine')


def send_data_to_arduino_engine(speed=None, rotation=None):
    logging.debug('@ send_data_to_arduino_engine')
    if not speed:
        speed = vars.engine_speed
    if not rotation:
        rotation = vars.rotation_angle
    logging.debug("Speed: {}, Rotation: {}".format(speed, rotation))
    vars.arduino_engine.send('s', speed)
    '''
    if rotation != consts.ROTATION[0]:
        vars.arduino_engine.send('r', rotation)
    else:
        vars.arduino_engine.send('s', speed)
    '''
    '''
    if rotation != consts.ROTATION[0]:
        if rotation != vars.lastrotation:
            vars.arduino_engine.send('r', rotation)
            vars.lastrotation = rotation
    else:
        if speed != vars.lastspeed:
            vars.arduino_engine.send('s', speed)
            vars.lastspeed = speed
    '''


    '''
    vars.arduino_engine.send('s', speed)
    vars.lastspeed = speed
    vars.arduino_engine.send('r', rotation)
    '''
    logging.debug('$ send_data_to_arduino_engine')


def read_client():
    logging.debug('@ read_client')
    data = vars.server.receive()
    if data:
        data = data.decode('ascii')
        logging.debug("Data: {}".format(data))
        # vars.client_last_answer = time.time()

        command = re.search(r'C.+?\n', data)
        if command:
            command = re.sub(r'[C\n]', '', command.group(0))
            logging.debug("Command: {}".format(command))
            print(command)
            execute_command(command)

        speed = re.search(r's.+?\n', data)
        if speed:
            speed = re.sub(r'[s\n]', '', speed.group(0))
            if speed:
                speed = int(speed)
            logging.debug("Speed: {}".format(speed))
            vars.engine_speed = speed

        rotation = re.search(r'r.+?\n', data)
        if rotation:
            rotation = re.sub(r'[r\n]', '', rotation.group(0))
            if rotation:
                rotation = int(rotation)
            logging.debug("Rotation: {}".format(rotation))
            vars.rotation_angle = rotation
    logging.debug('$ read_client')


def execute_command(command):
    try:
        vars.state = command_to_state[command]
    except KeyError:
        logging.warning("Unknown command: '{}'".format(command))


def send_ultrasonic_data():
    logging.debug('@ send_ultrasonic_data')
    vars.server.send('Q', vars.obstacle_distance_front_left)
    vars.server.send('L', vars.obstacle_distance_left)
    vars.server.send('R', vars.obstacle_distance_right)
    logging.debug('$ send_ultrasonic_data')


def actions_state_manual():
    logging.debug("@ actions_state_manual")
    if scripts.obstacle_is_at_front():
        #scripts.do_break()
        logging.debug("Obstacle is at front -> breaking")
    send_data_to_arduino_engine()
    logging.debug("$ actions_state_manual")


def actions_state_exit():
    logging.info("@ actions_state_exit")
    scripts.do_break()
    vars.arduino_sensors.close()
    vars.arduino_engine.close()
    vars.server.close()
    logging.info("$ actions_state_exit")
    quit(0)


def actions_state_auto():
    logging.debug("@ actions_state_auto")
    vars.state = consts.STATE_MANUAL
    logging.debug("State changed :: STATE_MANUAL")
    logging.debug("$ actions_state_auto")


def actions_state_reload():
    logging.info("@ actions_state_reload")
    vars.arduino_engine.reconnect()
    vars.arduino_sensors.reconnect()
    vars.state = consts.STATE_MANUAL
    logging.debug("State changed :: STATE_MANUAL")
    logging.info("$ actions_state_reload")


def actions_state_way():
    if not vars.wayflag:
        vars.ticker = time.time()
        vars.wayflag = True
        vars.wayflag1 = True

    if vars.wayflag1:
        if time.time() - vars.ticker > 0.15:
            vars.wayflag1 = False
            vars.ticker = time.time()
    else:
        if time.time() - vars.ticker > 0.3:
            vars.wayflag1 = True
            vars.ticker = time.time()

    res = scripts.move_through_the_corridor(vars.wayflag1)
    logging.debug("@ actions_state_way")
    if res == 1:
        vars.state = consts.STATE_MANUAL
        logging.debug("State changed :: STATE_MANUAL")
        vars.wayflag = False
    logging.debug("$ actions_state_way")


def actions_state_break():
    logging.debug("@ actions_state_break")
    scripts.do_break()
    vars.state = consts.STATE_MANUAL
    logging.debug("State changed :: STATE_MANUAL")
    logging.debug("$ actions_state_break")


command_to_state = {
    'Exit': consts.STATE_EXIT,
    'Auto': consts.STATE_AUTO,
    'Reload': consts.STATE_RELOAD,
    'Way': consts.STATE_WAY,
    'Pow': consts.STATE_BREAK
}
state_to_actions = {
    consts.STATE_MANUAL: actions_state_manual,
    consts.STATE_EXIT: actions_state_exit,
    consts.STATE_AUTO: actions_state_auto,
    consts.STATE_RELOAD: actions_state_reload,
    consts.STATE_WAY: actions_state_way,
    consts.STATE_BREAK: actions_state_break
}
