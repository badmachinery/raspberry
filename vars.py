import consts
import arduino_lib
import socket_connection


#arduino = arduino_lib.Arduino('/dev/ttyACM0')

arduino = arduino_lib.Arduino('/dev/ttyACM0')

server = socket_connection.SocketServer()

arduino_data = ''
arduino_last_update = 0

socket_data = ''
client_last_update = 0


sensor_front_data = 300
sensor_left_data = 300
sensor_right_data = 300

state = consts.state['manual']

engine_speed = consts.engine_speed[0]
rotation = consts.rotation[0]

engine_speed_max = 3

wayflag = False
wayflag1 = False
ticker = 0

lastspeed = consts.engine_speed[0]
lastrotation = consts.rotation[0]

stopper = 0
