from neopixel_helper import np, bright

sonar = microbit.pin15


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