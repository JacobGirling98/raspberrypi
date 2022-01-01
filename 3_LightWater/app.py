import RPi.GPIO as gpio
from time import sleep
import random
from dataclasses import dataclass
from enum import Enum

class LedState(Enum):
    ON = gpio.LOW
    OFF = gpio.HIGH


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


@dataclass(frozen=True)
class GenericLed:
    pin: int
    state: LedState


@dataclass(frozen=True)
class Trail():
    direction: int
    position: int


class Water:

    _pins = [
        GenericLed(11, LedState.OFF), 
        GenericLed(12, LedState.OFF), 
        GenericLed(13, LedState.OFF), 
        GenericLed(15, LedState.OFF), 
        GenericLed(16, LedState.OFF), 
        GenericLed(18, LedState.OFF),
        GenericLed(22, LedState.OFF),
        GenericLed(3, LedState.OFF),
        GenericLed(5, LedState.OFF),
        GenericLed(24, LedState.OFF)
    ]

    def _setup(self) -> None:
        gpio.setmode(gpio.BOARD)
        gpio.setup([x.pin for x in self._pins], gpio.OUT)
        gpio.output([x.pin for x in self._pins], gpio.HIGH)

    def _change_led_state(self, state: LedState) -> LedState:
        return LedState.OFF if state is LedState.ON else LedState.ON

    def _toggle_led(self, pin: GenericLed) -> GenericLed:
        state = self._change_led_state(pin.state)
        gpio.output(pin.pin, state.value)
        return GenericLed(pin.pin, state)

    def _toggle_led_from_trail(self, trail: Trail) -> None:
        pin = self._pins[trail.position]
        led_on = self._toggle_led(pin)
        sleep(0.05)
        self._toggle_led(led_on)

    def _random_motion(self):
        while True:
            position = random.randrange(0, 9)
            self._pins[position] = self._toggle_led(self._pins[position])
            sleep(0.1)

    def _move_trail(self, trail: Trail) -> Trail:
        direction = self._change_direction(trail.direction) if self._is_first_pin(trail) or self._is_last_pin(trail) else trail.direction
        position = trail.position + direction.value
        return Trail(direction, position) 

    def _is_last_pin(self, trail: Trail):
        return trail.position == len(self._pins) - 1 and trail.direction == Direction.RIGHT

    def _is_first_pin(self, trail: Trail):
        return trail.position == 0 and trail.direction == Direction.LEFT

    def _change_direction(self, direction: Direction) -> Direction:
        return Direction.LEFT if direction is Direction.RIGHT else Direction.RIGHT

    def _trail_motion(self):
        trail = Trail(Direction.RIGHT, 0)
        while True:
            self._toggle_led_from_trail(trail)
            trail = self._move_trail(trail)

    def _destroy(self):
        gpio.cleanup()

    def run(self):
        self._setup()
        try:
            # self._random_motion()
            self._trail_motion()
        except KeyboardInterrupt:
            self._destroy()
        except Exception as e:
            self._destroy()
            print(e)


if __name__ == "__main__":
    water = Water()
    water.run()