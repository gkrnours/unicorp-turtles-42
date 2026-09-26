import pyglet
from pyglet.math import Vec2

DEFAULT_SPEED = 6


class BadPaternException(Exception): ...


class Boss(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, *args, screen, **kwargs):
        x = screen.width / 2 - img.width / 2
        y = screen.height * 4 / 5

        super().__init__(img, x, y, *args, **kwargs)
        self.scale = 1 / 2

        self._screen = screen
        self._base_y = y
        self._pattern_pointer = 0
        self._pattern = [
            "GOTO -90",
            "GOTO 50% 10",
            "GOTO 90",
            "GOTO 50% 10",
        ]

    def update(self, dt):
        current_pattern = self._pattern[self._pattern_pointer]
        target = self.read_pattern(current_pattern)

        direction = target - self.position
        # move is a fraction of the direction based on the direction, speed and dt
        move = direction.normalize() * dt * 40 * self._speed
        # if we are close enough to destination, next part of the pattern
        if direction.length_squared() < move.length_squared():
            self._pattern_pointer = (self._pattern_pointer + 1) % len(self._pattern)
            return
        self.x += move.x
        self.y += move.y

    def read_pattern(self, pattern):
        match pattern.split():
            case ("GOTO", x):
                return self._read_goto(x, DEFAULT_SPEED)
            case ("GOTO", x, speed):
                return self._read_goto(x, float(speed))
        raise BadPaternException()

    def _read_goto(self, x, speed):
        self._speed = speed
        if x.endswith("%"):
            a = int(x[:-1])
            x = self._screen.width * a / 100
            return Vec2(x, self._base_y)

        if x.startswith("-"):
            x = self._screen.width - self.width - int(x[1:])
            return Vec2(x, self._base_y)

        return Vec2(int(x), self._base_y)
