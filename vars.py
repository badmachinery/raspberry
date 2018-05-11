import constants as c

obstacle_distance_front_left = 300
obstacle_distance_front_right = 300
obstacle_distance_left = 300
obstacle_distance_right = 300

state = c.STATE_MANUAL

current_time_sensors = 0
current_time_client = 0

arduino_sensors_last_answer = 0
arduino_engine_last_answer = 0
client_last_answer = 0

client_commands = []

engine_speed = c.ENGINE_SPEED[0]
rotation_angle = c.SERVO_ANGLE[0]
