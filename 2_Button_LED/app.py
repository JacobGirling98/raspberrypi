import RPi.GPIO as gpio


class LEDSwitch:

    def __init__(self, led_number: int, button_number: int):
        self.led = led_number
        self.button = button_number

    def _setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.led, gpio.OUT)
        gpio.setup(self.button, gpio.IN, pull_up_down=gpio.PUD_UP)

    def _teardown(self):
        gpio.cleanup()

    def _switch(self):
        while True:
            if gpio.input(self.button) == gpio.LOW:
                gpio.output(self.led, gpio.HIGH)
            else:
                gpio.output(self.led, gpio.LOW)

    def run(self):
        self._setup()
        try:
            print("Press button to turn on led")
            self._switch()
        except KeyboardInterrupt:
            self._teardown()
        except Exception as e:
            self._teardown()
            print(e)


if __name__ == "__main__":
    switch = LEDSwitch(
        led_number=11,
        button_number=12
    )
    switch.run()
