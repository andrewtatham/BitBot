def get_light():
    light_sensor_selection.write_digital(0)  # select left sensor
    left_light = light_sensor_intensity.read_analog()
    light_sensor_selection.write_digital(1)  # select right sensor
    right_light = light_sensor_intensity.read_analog()
    return left_light / 1023, right_light / 1023


light_sensor_intensity = microbit.pin2
light_sensor_selection = microbit.pin16