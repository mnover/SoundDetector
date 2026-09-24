from machine import Pin, ADC, I2C
import sh1106
import math
import time


# ============================================================
# OLED
# ============================================================

i2c = I2C(
    0,
    scl=Pin(9),
    sda=Pin(8),
    freq=100000
)

oled = sh1106.SH1106(
    128,
    64,
    i2c,
    addr=0x3C
)


# ============================================================
# MICROPHONES
#
# A = GPIO 39 =   0°
# B = GPIO 36 =  90°
# C = GPIO 35 = 180°
# D = GPIO 34 = 270°
# ============================================================

mic_a = ADC(Pin(39))
mic_b = ADC(Pin(36))
mic_c = ADC(Pin(35))
mic_d = ADC(Pin(34))


# Configure ADC range
# 0-3.3V range on ESP32
mic_a.atten(ADC.ATTN_11DB)
mic_b.atten(ADC.ATTN_11DB)
mic_c.atten(ADC.ATTN_11DB)
mic_d.atten(ADC.ATTN_11DB)


SENSOR_ANGLES = {
    'a': 0,
    'b': 90,
    'c': 180,
    'd': 270
}


# ============================================================
# READ MICROPHONES
# ============================================================

def read_mics():

    a = mic_a.read()
    b = mic_b.read()
    c = mic_c.read()
    d = mic_d.read()

    return {
        'a': a,
        'b': b,
        'c': c,
        'd': d
    }


# ============================================================
# FIND TWO LOUDEST MICROPHONES
# ============================================================

def loudest_sensors(readings):

    sorted_sensors = sorted(
        readings.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_sensors[0], sorted_sensors[1]


# ============================================================
# CALCULATE DIRECTION
# ============================================================

def calculate_direction(sensor_list):

    sensor1 = sensor_list[0][0]
    sensor2 = sensor_list[1][0]

    value1 = sensor_list[0][1]
    value2 = sensor_list[1][1]

    pair = {sensor1, sensor2}


    # A → B
    if pair == {'a', 'b'}:

        low_sensor = 'a'
        high_sensor = 'b'
        start_angle = 0


    # B → C
    elif pair == {'b', 'c'}:

        low_sensor = 'b'
        high_sensor = 'c'
        start_angle = 90


    # C → D
    elif pair == {'c', 'd'}:

        low_sensor = 'c'
        high_sensor = 'd'
        start_angle = 180


    # D → A
    elif pair == {'d', 'a'}:

        low_sensor = 'd'
        high_sensor = 'a'
        start_angle = 270


    else:
        return None


    # Put the readings in the correct order
    if sensor1 == low_sensor:

        low_value = value1
        high_value = value2

    else:

        low_value = value2
        high_value = value1


    total = low_value + high_value

    if total == 0:
        return None


    # Weighted position between the two microphones
    ratio = high_value / total

    direction = start_angle + ratio * 90

    return direction % 360


# ============================================================
# OLED ARROW
#
# 0°   = UP
# 90°  = RIGHT
# 180° = DOWN
# 270° = LEFT
# ============================================================

def draw_arrow(angle):

    oled.fill(0)

    cx = 64
    cy = 32

    length = 25

    radians = math.radians(angle)

    x = int(
        cx + length * math.sin(radians)
    )

    y = int(
        cy - length * math.cos(radians)
    )


    # Main arrow shaft
    oled.line(
        cx,
        cy,
        x,
        y,
        1
    )


    # Arrow head
    head_length = 8
    head_angle = 30

    angle1 = math.radians(
        angle + head_angle
    )

    angle2 = math.radians(
        angle - head_angle
    )


    x1 = int(
        x - head_length * math.sin(angle1)
    )

    y1 = int(
        y + head_length * math.cos(angle1)
    )


    x2 = int(
        x - head_length * math.sin(angle2)
    )

    y2 = int(
        y + head_length * math.cos(angle2)
    )


    oled.line(
        x,
        y,
        x1,
        y1,
        1
    )

    oled.line(
        x,
        y,
        x2,
        y2,
        1
    )


    # Center point
    oled.pixel(
        cx,
        cy,
        1
    )

    oled.show()


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # Read all four microphones
    readings = read_mics()


    # Get two strongest microphones
    loudest = loudest_sensors(readings)


    # Calculate direction
    direction = calculate_direction(loudest)


    # Display direction if valid
    if direction is not None:

        draw_arrow(direction)


    # Serial output for debugging
    print(
        "A:", readings['a'],
        "B:", readings['b'],
        "C:", readings['c'],
        "D:", readings['d'],
        "| Loudest:", loudest,
        "| Direction:", direction
    )


    time.sleep_ms(100)