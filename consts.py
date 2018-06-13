state = {
'manual': 0,
'auto': 1,
'break': 2,
'way': 3,
'exit': 4,
'reload': 5,
}

command_symbol_arduino = {
'sensor_forward': 'F',
'sensor_left': 'L',
'sensor_right': 'R',
}

command_symbol_client = {
'exit': 'E',
'reload': 'R',
'way': 'W',
'forward': 'F',
'backward': 'B',
'stay': 'S',
'speed_up': '+',
'speed_down': '-',
'left': 'L',
'right': 'R',
'middle': 'M'
}

command_group = {
'arduino': (command_symbol_arduino['sensor_forward'], command_symbol_arduino['sensor_left'], command_symbol_arduino['sensor_right']),
'sensors': (command_symbol_arduino['sensor_forward'], command_symbol_arduino['sensor_left'], command_symbol_arduino['sensor_right']),
'client': (
        command_symbol_client['forward'], command_symbol_client['backward'],
        command_symbol_client['stay'], command_symbol_client['speed_up'],
        command_symbol_client['speed_down'], command_symbol_client['left'],
        command_symbol_client['right'], command_symbol_client['middle'],
        command_symbol_client['exit'], command_symbol_client['reload'],
        command_symbol_client['way']
    ),
'manual': (
        command_symbol_client['forward'], command_symbol_client['backward'],
        command_symbol_client['stay'], command_symbol_client['speed_up'],
        command_symbol_client['speed_down'], command_symbol_client['left'],
        command_symbol_client['right'], command_symbol_client['middle']
    ),
}


reconnection_time = 0.5
lost_connection_time = 0.5

avoidance_distance = 20

engine_speed = {
-3: -100,
-2: -66,
-1: -33,
0: 0,
1: 33,
2: 66,
3: 100,
}

rotation = {
-3: -100,
-2: -66,
-1: -33,
0: 0,
1: 33,
2: 66,
3: 100
}

ENGINE_SPEED_OLD = {
-3: 5696,
-2: 6196,
-1: 6696,
0: 7200,
1: 7453,
2: 7710,
3: 7967,
}

SERVO_ANGLE_OLD = {
45: 2800,
30: 7036,
15: 7423,
0: 7810,
-15: 8360,
-30: 8910,
-45: 4400
}
