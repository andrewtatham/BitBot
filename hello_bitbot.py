import microbit

if __name__ == '__main__':
    microbit.display.scroll("HELLO")
    while True:
        microbit.display.show(microbit.Image.HAPPY)
        microbit.sleep(200)
