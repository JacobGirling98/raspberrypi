import RPi.GPIO as gpio
from time import sleep
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class LedState:
    number: int
    state: gpio.LOW or gpio.HIGH


class Water:

    _pins = [
        LedState(11, gpio.HIGH), 
        LedState(12, gpio.HIGH), 
        LedState(13, gpio.HIGH), 
        LedState(15, gpio.HIGH), 
        LedState(16, gpio.HIGH), 
        LedState(18, gpio.HIGH),
        LedState(22, gpio.HIGH),
        LedState(3, gpio.HIGH),
        LedState(5, gpio.HIGH),
        LedState(24, gpio.HIGH)
    ]

    def _setup(self) -> None:
        gpio.setmode(gpio.BOARD)
        gpio.setup([x.number for x in self._pins], gpio.OUT)
        gpio.output([x.number for x in self._pins], gpio.HIGH)

    def _toggle_led(self, pin: LedState) -> LedState:
        state = gpio.HIGH if pin.state == gpio.LOW else gpio.LOW
        gpio.output(pin.number, state)
        return LedState(pin.number, state)

    def _random_motion(self):
        while True:
            position = random.randrange(0, 9)
            self._pins[position] = self._toggle_led(self._pins[position])
            sleep(0.1)

    def _destroy(self):
        gpio.cleanup()

    def run(self):
        self._setup()
        try:
            self._random_motion()
        except KeyboardInterrupt:
            self._destroy()
        except Exception as e:
            self._destroy()
            print(e)


if __name__ == "__main__":
    water = Water()
    water.run()