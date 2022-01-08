import RPi.GPIO as gpio
from time import sleep
import random
from dataclasses import dataclass
from enum import Enum


class Breath:

    pwm: gpio.PWM

    def __init__(self, led: int = 12):
        self.led = led

    def _setup(self) -> None:
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.led, gpio.OUT)
        gpio.output(self.led, gpio.HIGH)

        self.pwm = gpio.PWM(self.led, 500)
        self.pwm.start(0)

    def _turn_on(self) -> None:
        for dc in range(101):
            self.pwm.ChangeDutyCycle(dc)
            sleep(0.01)

    def _turn_off(self) -> None:
        for dc in range(100, -1, -1):
            self.pwm.ChangeDutyCycle(dc)
            sleep(0.01)

    def _breath(self) -> None:
        while True:
            sleep(1)
            self._turn_on()
            sleep(1)
            self._turn_off()

    def _destroy(self) -> None:
        self.pwm.stop()
        gpio.cleanup()

    def run(self) -> None:
        self._setup()
        try:
            self._breath()
        except KeyboardInterrupt:
            self._destroy()
        except Exception as e:
            self._destroy()
            print(e)


if __name__ == "__main__":
    breath = Breath()
    breath.run()