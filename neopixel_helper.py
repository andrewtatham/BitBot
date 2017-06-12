import neopixel

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