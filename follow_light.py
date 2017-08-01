import microbit
import neopixel

numpixels = 12
np = neopixel.NeoPixel(microbit.pin13, numpixels)
bright = 8

light_sensor_intensity = microbit.pin2
light_sensor_selection = microbit.pin16

left_motor_speed = microbit.pin0
left_motor_direction = microbit.pin8
right_motor_speed = microbit.pin1
right_motor_direction = microbit.pin12

prev_left_np_id = None
prev_right_np_id = None


def constrain(min_value=0.0, value=0.0, max_value=1.0):
    return max(min_value, min(value, max_value))


def colour(factor):
    r = int(bright * factor)
    g = int(bright * (1.0 - factor))
    b = 0
    return r, g, b


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


def get_light():
    light_sensor_selection.write_digital(0)  # select left sensor
    left_light = light_sensor_intensity.read_analog()
    light_sensor_selection.write_digital(1)  # select right sensor
    right_light = light_sensor_intensity.read_analog()
    return left_light / 1023, right_light / 1023


def motors(left_factor, right_factor):
    # accepts -1.0 to +1.0
    left_direction = left_factor < 0
    right_direction = right_factor < 0
    if left_direction:
        # Reverse
        l = constrain(0, 1023 + left_factor * 1023, 1023)
    else:
        l = constrain(0, left_factor * 1023, 1023)
    if right_direction:
        r = constrain(0, 1023 + right_factor * 1023, 1023)
    else:
        r = constrain(0, right_factor * 1023, 1023)
    left_motor_direction.write_digital(left_direction)
    left_motor_speed.write_analog(l)
    right_motor_direction.write_digital(right_direction)
    right_motor_speed.write_analog(r)


if __name__ == '__main__':

    left_speed = 0
    right_speed = 0

    microbit.display.scroll("HELLO")
    while True:
        left_speed, right_speed = get_light()
        dual_scale(left_speed, right_speed, 1.0)
        diff = left_speed - right_speed
        avg = (left_speed + right_speed) / 2
        fwd = 0.5
        steer = 2.0
        left_speed = steer * diff
        right_speed = - steer * diff
        # motors(left_speed, right_speed)

        # ramp()
        microbit.display.show(microbit.Image.HAPPY)
        microbit.sleep(100)
