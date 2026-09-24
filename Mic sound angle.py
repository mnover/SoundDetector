from machine import ADC, Pin
import time

#a = ADC(Pin(36, Pin.IN, Pin.PULL_DOWN))
#b = ADC(Pin(39, Pin.IN, Pin.PULL_DOWN))
#c = ADC(Pin(34, Pin.IN, Pin.PULL_DOWN))
#d = ADC(Pin(35, Pin.IN, Pin.PULL_DOWN))

a = ADC(Pin(0, Pin.IN, Pin.PULL_DOWN))
b = ADC(Pin(1, Pin.IN, Pin.PULL_DOWN))
c = ADC(Pin(3, Pin.IN, Pin.PULL_DOWN))
d = ADC(Pin(4, Pin.IN, Pin.PULL_DOWN))


A = a.read()
B = b.read()
C = c.read()
D = d.read()

sens_list = loudest_sens(A,B,C,D)
sens_range = angle_range(sens_list)
direct = direction(sens_list, sens_range)

print("assuming sensor a faces 0 degrees, sensor b faces 90 degrees, c:180, d:270, the sound came from ", direct, "degrees")

def loudest_sens(a,b,c,d):
    
    raw_sound_dic = {'a':a, 'b':b, 'c':c, 'd':d}
    
    sorted_dic = sorted(raw_sound_dic.items(), key=lambda x: x[1], reverse=True)
    
    uno = sorted_dic[0]
    dos = sorted_dic[1]
    
    return uno, dos

def angle_range(sens_list):
    
    sensors = {sens_list[0][0], sens_list[1][0]}
    
    if sensors == {'a', 'b'}: sens_range = [0, 90]
    elif sensors == {'b', 'c'}: sens_range = [90, 180]
    elif sensors == {'c', 'd'}: sens_range = [180, 270]
    elif sensors == {'d', 'a'}: sens_range = [270, 360]
    else: pass
    
    return sens_range

def direction(sens_list, sens_range):

    sensor1 = sens_list[0][0]
    sensor2 = sens_list[1][0]

    value1 = sens_list[0][1]
    value2 = sens_list[1][1]

    low_angle_sensor = None
    high_angle_sensor = None

    # Determine which sensor is at the lower angle
    if {sensor1, sensor2} == {'a', 'b'}:
        low_angle_sensor = 'a'
        high_angle_sensor = 'b'

    elif {sensor1, sensor2} == {'b', 'c'}:
        low_angle_sensor = 'b'
        high_angle_sensor = 'c'

    elif {sensor1, sensor2} == {'c', 'd'}:
        low_angle_sensor = 'c'
        high_angle_sensor = 'd'

    elif {sensor1, sensor2} == {'d', 'a'}:
        low_angle_sensor = 'd'
        high_angle_sensor = 'a'

    # Get the readings corresponding to the low/high sensors
    if sensor1 == low_angle_sensor:
        low_value = value1
        high_value = value2
    else:
        low_value = value2
        high_value = value1

    # Calculate position within the 90 degree range
    ratio = high_value / (low_value + high_value)

    direction = sens_range[0] + ratio * 90

    return direction