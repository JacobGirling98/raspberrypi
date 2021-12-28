import RPi.GPIO as gpio
import time


class Blinker:

    def __init__(self, pin_number: int):
        self.pin = pin_number
        
    def _setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, gpio.LOW)
        print(f"Using pin {self.pin}")

    def _teardown(self):
        gpio.cleanup()

    def _blink(self):
        while True:
                gpio.output(self.pin, gpio.HIGH)
                print("LED on >>>")
                time.sleep(1)
                gpio.output(self.pin, gpio.LOW)
                print("LED off <<<")
                time.sleep(1)

    def run(self):
        self._setup()
        try:
            self._blink()
        except KeyboardInterrupt:
            self._teardown()
        except Exception:
            self._teardown()


if __name__ == "__main__":
    blinker = Blinker(11)
    blinker.run()
