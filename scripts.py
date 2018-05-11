from arduino_lib import arduino_sensors, arduino_engine
import constants as c
import vars as v
import time

def move(speed, rotation, seconds):
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

def simple_front_obstacle_evasion():
    ''' moving in every state '''
    print('Simple front obstacle evasion ::: start')
    #stop()
    #move(c.ENGINE_SPEED[0], c.SERVO_ANGLE[0], 0.5)
    while (v.obstacle_distance_front_left < c.AVOIDANCE_DISTANCE or v.obstacle_distance_front_right < c.AVOIDANCE_DISTANCE):
        move(c.ENGINE_SPEED[-1], c.SERVO_ANGLE[0], 0.2)
    print('Simple front obstacle evasion ::: done')
    v.state = c.STATE_MANUAL

def custom_script():
    print('Custom script')
    print('Done')
