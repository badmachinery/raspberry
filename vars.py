import consts
import arduino_lib
import socket_connection

arduino_sensors = arduino_lib.Arduino('/dev/ttyACM0')
# arduino_sensors_last_answer_time = 0

arduino_engine = arduino_lib.Arduino('/dev/ttyACM1')
# arduino_engine_last_answer_time = 0

server = socket_connection.SocketServer()
# client_last_answer_time = 0

obstacle_distance_front_left = 300
obstacle_distance_front_right = 300
obstacle_distance_left = 300
obstacle_distance_right = 300

state = consts.STATE_MANUAL

engine_speed = consts.ENGINE_SPEED[0]
rotation_angle = consts.SERVO_ANGLE[0]

wayflag = False
wayflag1 = False
ticker = 0


lastspeed = consts.ENGINE_SPEED[0]

stopper = 0

