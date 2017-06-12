import microbit

# Buttons / Line Sensors (Shared pins)
button_a = microbit.pin5
button_b = microbit.pin11
left_line_sensor = microbit.pin11
right_line_sensor = microbit.pin5



def display_compass_heading():
    needle = ((15 - microbit.compass.heading()) // 30) % 12
    microbit.display.show(microbit.Image.ALL_CLOCKS[needle])
    return needle


def get_accelerometer():
    x, y, z = microbit.accelerometer.get_values()
    return x, y, z


def get_gesture():
    gesture = microbit.accelerometer.current_gesture()
    # up, down, left, right, face up, face down, freefall, 3g, 6g, 8g, shake
    if gesture == "face up":
        microbit.display.show(microbit.Image.HAPPY)
    else:
        microbit.display.show(microbit.Image.ANGRY)
    return gesture


def get_buttons():
    a = microbit.button_a.is_pressed()
    b = microbit.button_b.is_pressed()
    if a and b:
        microbit.display.scroll("AB")
    elif a:
        microbit.display.scroll("A")
    elif b:
        microbit.display.scroll("B")
    return a, b


while True:
    # dance()

    # display_compass_heading()

    a, b = get_buttons()

    # d = get_distance()
    # print(d)
    # single_scale(d, 25)
    #
    # l, r = get_light()
    # diff = l - r
    # avg = (l + r) / 2
    # fwd = 0.1
    # steer = 2.0
    # l = steer * diff
    # r = - steer * diff
    # dual_scale(l, r, 1.0)
    # motors(l, r)

    # ramp()
    microbit.sleep(100)
