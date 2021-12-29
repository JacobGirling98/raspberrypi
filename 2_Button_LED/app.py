import RPi.GPIO as gpio


class LEDSwitch:

    _led_is_on = False
    _mode: str = None

    def __init__(self, led_number: int, button_number: int):
        self._led = led_number
        self._button = button_number

    def _setup(self) -> None:
        gpio.setmode(gpio.BOARD)
        gpio.setup(self._led, gpio.OUT)
        gpio.setup(self._button, gpio.IN, pull_up_down=gpio.PUD_UP)
        self._mode = input("hold or click:\n")
        
    def _teardown(self) -> None:
        gpio.cleanup()

    def _on_click(self, channel) -> None:
        self._led_is_on = not self._led_is_on
        print("LED turned on" if self._led_is_on else "LED turned off")
        gpio.output(self._led, self._led_is_on)

    def _hold_button(self) -> None:
        print("\nHold button for LED")
        while True:
            if gpio.input(self._button) == gpio.LOW:
                gpio.output(self._led, gpio.HIGH)
            else:
                gpio.output(self._led, gpio.LOW)

    def _click_button(self) -> None:
        print("\nClick button for LED")
        gpio.add_event_detect(self._button, gpio.FALLING, callback=self._on_click, bouncetime=300)
        while True: pass

    def run(self) -> None:
        self._setup()
        try:
            if self._mode == "hold":
                self._hold_button()
            elif self._mode == "click":
                self._click_button()
            else:
                raise Exception("Enter valid mode")
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
