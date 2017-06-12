from neopixel_helper import constrain

left_motor_speed = microbit.pin0
left_motor_direction = microbit.pin8
right_motor_speed = microbit.pin1
right_motor_direction = microbit.pin12


def forward(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_N)
    motors(speed, speed)
    microbit.sleep(time)


def reverse(time=1000, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_S)
    motors(-speed, -speed)
    microbit.sleep(time)


def left(time=240, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_W)
    motors(-speed, speed)
    microbit.sleep(time)


def right(time=240, speed=1.0):
    microbit.display.show(microbit.Image.ARROW_E)
    motors(speed, -speed)
    microbit.sleep(time)


def stop(time=1000):
    microbit.display.show(microbit.Image.SQUARE_SMALL)
    motors(0, 0)
    microbit.sleep(time)


def motors(left_factor, right_factor):
    # accepts -1.0 to +1.0
    left_direction = left_factor < 0
    right_direction = right_factor < 0
    if left_direction:
        # Reverse
        left_speed = constrain(0, 1023 + left_factor * 1023, 1023)
    else:
        left_speed = constrain(0, left_factor * 1023, 1023)
    if right_direction:
        right_speed = constrain(0, 1023 + right_factor * 1023, 1023)
    else:
        right_speed = constrain(0, right_factor * 1023, 1023)
    left_motor_direction.write_digital(left_direction)
    left_motor_speed.write_analog(left_speed)
    right_motor_direction.write_digital(right_direction)
    right_motor_speed.write_analog(right_speed)


def dance():
    forward()
    left()
    forward()
    right()
    forward()
    stop()
    reverse()
    stop()