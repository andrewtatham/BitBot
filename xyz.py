import microbit
import neopixel
from random import randint

# Buttons / Line Sensors (Shared pins)
button_a = microbit.pin5
button_b = microbit.pin11
left_line_sensor = microbit.pin11
right_line_sensor = microbit.pin5

# Motors
left_motor_speed = microbit.pin0
left_motor_direction = microbit.pin8
right_motor_speed = microbit.pin1
right_motor_direction = microbit.pin12

# Light Sensors
light_sensor_intensity = microbit.pin2
light_sensor_selection = microbit.pin16

# Buzzer
buzzer = microbit.pin14

# Ultrasonic Sensor
sonar = microbit.pin15

# Neopixels
numpixels = 12
np = neopixel.NeoPixel(microbit.pin13, numpixels)
bright = 8


def constrain(min_value=0.0, value=0.0, max_value=1.0):
    return max(min_value, min(value, max_value))


def colour(factor):
    r = int(bright * factor)
    g = int(bright * (1.0 - factor))
    b = 0
    return r, g, b


prev_np_id = None


def single_scale(value, max_value=1.0):
    global prev_np_id
    factor = constrain(0.0, value / max_value, 1.0)
    np_id = constrain(0, int(6.0 * factor), 5)
    rgb = colour(factor)
    if prev_np_id is not None:
        np[prev_np_id] = (0, 0, 0)
    np[np_id] = rgb
    np.show()
    prev_np_id = np_id


prev_left_np_id = None
prev_right_np_id = None


def dual_scale(left_value, right_value, max_value=1.0):
    global prev_left_np_id
    global prev_right_np_id
    left_factor = constrain(0.0, left_value / max_value, 1.0)
    right_factor = constrain(0.0, right_value / max_value, 1.0)
    left_np_id = constrain(0, int(6.0 * left_factor), 5)
    right_np_id = constrain(6, int(6.0 * right_factor) + 6, 11)
    left_rgb = colour(left_factor)
    right_rgb = colour(right_factor)
    if prev_left_np_id is not None:
        np[prev_left_np_id] = (0, 0, 0)
    if prev_right_np_id is not None:
        np[prev_right_np_id] = (0, 0, 0)
    np[left_np_id] = left_rgb
    np[right_np_id] = right_rgb
    np.show()
    prev_left_np_id = left_np_id
    prev_right_np_id = right_np_id


def get_distance():
    np[7] = (0, 0, bright)
    np.show()

    timeout = False
    start = microbit.running_time()
    rising_edge = start
    falling_edge = start

    sonar.write_digital(0)
    microbit.sleep(1000)
    sonar.write_digital(1)  # Send 10us pulse to trigger
    microbit.sleep(0.01)
    sonar.write_digital(0)

    while sonar.read_digital() == 0 and not timeout:
        rising_edge = microbit.running_time()
    while sonar.read_digital() == 1 and not timeout:
        falling_edge = microbit.running_time()

    if timeout:
        distance = 0
        np[7] = (bright, 0, 0)
    else:
        pulse_width = falling_edge - rising_edge
        distance = pulse_width * 17150
        np[7] = (0, bright, 0)
    np.show()
    return int(distance)


def get_light():
    light_sensor_selection.write_digital(0)  # select left sensor
    left_light = light_sensor_intensity.read_analog()
    light_sensor_selection.write_digital(1)  # select right sensor
    right_light = light_sensor_intensity.read_analog()
    return left_light / 1024, right_light / 1024


def forward(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_N)
    motors(speed, speed)
    microbit.sleep(time)


def reverse(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_S)
    motors(-speed, -speed)
    microbit.sleep(time)


def left(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_E)
    motors(-speed, speed)
    microbit.sleep(time)


def right(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_W)
    motors(speed, -speed)
    microbit.sleep(time)


def stop():
    microbit.display.show(microbit.Image.SQUARE_SMALL)
    motors(0, 0)


def motors(left_factor, right_factor):
    # accepts -1.0 to +1.0
    left_direction = left_factor < 0
    right_direction = right_factor < 0
    left_speed = constrain(0, abs(left_factor) * 1024, 1023)
    right_speed = constrain(0, abs(right_factor) * 1024, 1023)
    left_motor_speed.write_analog(left_speed)
    left_motor_direction.write_digital(left_direction)
    right_motor_speed.write_analog(right_speed)
    right_motor_direction.write_digital(right_direction)


def blip():
    buzzer.write_digital(1)
    microbit.sleep(20)
    buzzer.write_digital(0)


def ramp():
    for i in range(1024):
        single_scale(i, 1024)
        buzzer.write_analog(i)
        microbit.sleep(20)
        buzzer.write_digital(0)
        microbit.sleep(1000)


def dance():
    forward()
    left()
    forward()
    right()
    forward()
    reverse()
    stop()


while True:
    # d = get_distance()
    # print(d)
    # single_scale(d, 25)

    l, r = get_light()
    dual_scale(l, r, 1.0)
    # motors(l, r)

    # ramp()
    microbit.sleep(100)
