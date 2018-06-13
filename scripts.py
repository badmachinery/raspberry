import time
import logging

import consts
import vars
import actions
from utility import log

mark = 0
flag = False


def obstacle_is_at_front(distance=consts.avoidance_distance):
    return 1 < vars.sensor_front_data < distance


def obstacle_is_at_left(distance=consts.avoidance_distance):
    return 1 < vars.sensor_left_data < distance


def obstacle_is_at_right(distance=consts.avoidance_distance):
    return 1 < vars.sensor_right_data < distance


#@log
def move(speed, rotation, seconds=0.1):
    if time.time() - mark < seconds:
        logging.debug("Continue moving")
        actions.send_data_to_arduino(speed, rotation)
        return False
    else:
        logging.debug('Stop moving')
        return True


#@log
def stop():
    actions.send_data_to_arduino(consts.engine_speed[0], consts.rotation[0])


#@log
def move_through_the_corridor():
    if not obstacle_is_at_front(50):
        logging.debug('No obstacle at front -> moving further')
        speed = consts.engine_speed[3]
        rotation = consts.rotation[0]
        if vars.sensor_right_data == 1:
            vars.sensor_right_data = 500
        if vars.sensor_left_data == 1:
            vars.sensor_left_data = 500
        if vars.sensor_left_data < vars.sensor_right_data:
            if vars.sensor_left_data < 40:
                rotation = consts.rotation[1]
                print('r')
                logging.debug("Rotating to right")
            elif 40 < vars.sensor_left_data < 70:
                rotation = consts.rotation[0]
                logging.debug("No rotation")
                print('f')
            else:
                rotation = consts.rotation[-1]
                logging.debug("Rotating to left")
                print('l')
        elif vars.sensor_left_data > vars.sensor_right_data:
            if vars.sensor_right_data < 40:
                rotation = consts.rotation[-1]
                logging.debug("Rotating to left")
                print('l')
            elif 40 < vars.sensor_right_data < 70:
                rotation = consts.rotation[0]
                logging.debug("No rotation")
                print('f')
            else:
                rotation = consts.rotation[1]
                logging.debug("Rotating to right")
                print('r')
        else:
            rotation = consts.rotation[0]
            logging.debug("No rotation")
            print('f')

        actions.send_data_to_arduino(speed, rotation)
        return False
    else:
        return True
