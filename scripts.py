import time
import logging

import consts
import vars
import actions

mark = 0


def obstacle_is_at_front_left(distance=consts.AVOIDANCE_DISTANCE):
    return 1 < vars.obstacle_distance_front_left < distance


def obstacle_is_at_front_right(distance=consts.AVOIDANCE_DISTANCE):
    return 1 < vars.obstacle_distance_front_right < distance


def obstacle_is_at_front(distance=consts.AVOIDANCE_DISTANCE):
    return obstacle_is_at_front_left(distance) or obstacle_is_at_front_right(distance)


def obstacle_is_at_front_both(distance=consts.AVOIDANCE_DISTANCE):
    return obstacle_is_at_front_left(distance) and obstacle_is_at_front_right(distance)


def obstacle_is_at_left(distance=consts.AVOIDANCE_DISTANCE):
    return 1 < vars.obstacle_distance_left < distance


def obstacle_is_at_right(distance=consts.AVOIDANCE_DISTANCE):
    return 1 < vars.obstacle_distance_right < distance


def move(speed, rotation, seconds=0.1):
    logging.debug("@ move")
    if time.time() - mark < seconds:
        logging.debug("Continue moving")
        actions.send_data_to_arduino_engine(speed, rotation)
        return False
    else:
        logging.debug('Stop moving')
        return True


def do_break():
    logging.debug("@ do_break")
    t = time.time()
    while time.time() - t < 0.3:    # Blocks everything, breaking has the highest priority
        actions.send_data_to_arduino_engine(consts.ENGINE_SPEED[-3], consts.SERVO_ANGLE[0])
    logging.debug('$ do_break')


# def stop():
    # Can't really stop without encoders
    # do_break()

'''
def simple_front_obstacle_evasion(new_state = c.STATE_BACK, last_state = c.STATE_MANUAL):
    print('Simple front obstacle evasion ::: start')
    v.state = new_state
    #TODO need to stop before
    while (v.obstacle_distance_front_left < c.AVOIDANCE_DISTANCE or v.obstacle_distance_front_right < c.AVOIDANCE_DISTANCE):
        if v.state != c.STATE_ALGORITHM:
            move(c.ENGINE_SPEED[-1], c.SERVO_ANGLE[0], 0.1)
            #do_break(seconds=0.05)
    print('Simple front obstacle evasion ::: done')
    v.state = last_state
'''

def move_through_the_corridor():
    logging.debug('@ move_through_the_corridor')
    if not obstacle_is_at_front(50):
        logging.debug('No obstacle at front -> moving further')
        speed = consts.ENGINE_SPEED[1]
        rotation = consts.SERVO_ANGLE[0]
        if vars.obstacle_distance_left < vars.obstacle_distance_right:
            if vars.obstacle_distance_left < 40:
                rotation = consts.SERVO_ANGLE[30]
                logging.debug("Rotating to right")
            elif 40 < vars.obstacle_distance_left < 70:
                rotation = consts.SERVO_ANGLE[0]
                logging.debug("No rotation")
            else:
                rotation = consts.SERVO_ANGLE[-30]
                logging.debug("Rotating to left")
        elif vars.obstacle_distance_left > vars.obstacle_distance_right:
            if vars.obstacle_distance_right < 40:
                rotation = consts.SERVO_ANGLE[-30]
                logging.debug("Rotating to left")
            elif 40 < vars.obstacle_distance_right < 70:
                rotation = consts.SERVO_ANGLE[0]
                logging.debug("No rotation")
            else:
                rotation = consts.SERVO_ANGLE[30]
                logging.debug("Rotating to right")
        else:
            rotation = consts.SERVO_ANGLE[0]
            logging.debug("No rotation")

        actions.send_data_to_arduino_engine(speed, rotation)

        logging.debug("Sensors info: {}, {}, {}, {}".format(vars.obstacle_distance_front_left, vars.obstacle_distance_front_right,
                                                            vars.obstacle_distance_left, vars.obstacle_distance_right))
        return 1
    else:
        do_break()
        logging.debug('Obstacle is at front -> stop moving')
        return 0
