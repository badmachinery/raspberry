import time

from arduino_lib import arduino_sensors, arduino_engine
import constants as c
import vars as v
import actions

def obstacle_is_at_front_left(distance=c.AVOIDANCE_DISTANCE):
    return 1 < v.obstacle_distance_front_left < distance

def obstacle_is_at_front_right(distance=c.AVOIDANCE_DISTANCE):
    return 1 < v.obstacle_distance_front_right < distance

def obstacle_is_at_front(distance=c.AVOIDANCE_DISTANCE):
    return obstacle_is_at_front_left(distance) or obstacle_is_at_front_right(distance)

def obstacle_is_at_front_both(distance=c.AVOIDANCE_DISTANCE):
    return obstacle_is_at_front_left(distance) and obstacle_is_at_front_right(distance)

def obstacle_is_at_left(distance=c.AVOIDANCE_DISTANCE):
    return 1 < v.obstacle_distance_left < distance

def obstacle_is_at_right(distance=c.AVOIDANCE_DISTANCE):
    return 1 < v.obstacle_distance_right < distance

def move(speed, rotation, seconds=0.1):
    ''' moving only in auto state '''
    t = time.time()
    while time.time() - t < seconds:
        if v.state == c.STATE_AUTO or v.state == c.STATE_BACK:
            arduino_engine.send('s', speed)
            arduino_engine.send('r', rotation)
        else:
            return False

def do_break(power=1200, seconds=0.5):
    ''' moving in every state '''
    print('Breaking: {}, {}s'.format(power, seconds))
    t = time.time()
    while time.time() - t < seconds:
        arduino_engine.send('b', power)
        arduino_engine.send('r', c.SERVO_ANGLE[0])

def stop():
    ''' TODO we should take encoders' data into a point '''
    print('Trying to stop')
    do_break(seconds=0.5)

def simple_front_obstacle_evasion(new_state = c.STATE_BACK, last_state = c.STATE_MANUAL):
    ''' moving in every state but algorithm '''
    print('Simple front obstacle evasion ::: start')
    v.state = new_state
    #TODO need to stop before
    while (v.obstacle_distance_front_left < c.AVOIDANCE_DISTANCE or v.obstacle_distance_front_right < c.AVOIDANCE_DISTANCE):
        if v.state != c.STATE_ALGORITHM:
            move(c.ENGINE_SPEED[-1], c.SERVO_ANGLE[0], 0.2)
    print('Simple front obstacle evasion ::: done')
    v.state = last_state

def move_through_the_corridor(new_state = c.STATE_ALGORITHM, last_state = c.STATE_MANUAL):
    '''moving in auto state'''
    print('Moving through the corridor ::: start')
    v.state = new_state
    while not obstacle_is_at_front():
        speed = c.ENGINE_SPEED[0]
        if v.obstacle_distance_left < v.obstacle_distance_right:
            if obstacle_is_at_left(40):
                rotation = c.SERVO_ANGLE[15]
            elif 40 < v.obstacle_distance_left < 70:
                rotation = c.SERVO_ANGLE[0]
            else:
                rotation = c.SERVO_ANGLE[-15]
        else:
            if obstacle_is_at_right(40):
                rotation = c.SERVO_ANGLE[-15]
            elif 40 < v.obstacle_distance_right < 70:
                rotation = c.SERVO_ANGLE[0]
            else:
                rotation = c.SERVO_ANGLE[15]
        move(speed, rotation)
    print('Done')
    v.state = last_state

def custom_script():
    print('Custom script')
    print('Done')
