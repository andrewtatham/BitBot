from neopixel_helper import single_scale

buzzer = microbit.pin14


def blip():
    buzzer.write_digital(1)
    microbit.sleep(20)
    buzzer.write_digital(0)


def ramp():
    for i in range(1024):
        single_scale(i, 1023)
        buzzer.write_analog(i)
        microbit.sleep(20)
        buzzer.write_digital(0)
        microbit.sleep(1000)