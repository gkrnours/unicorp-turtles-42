from random import random

import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors

DEFAULT_SPEED = 6


class BadPaternException(Exception): ...


class Boss(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, *args, screen, spawner, **kwargs):
        x = screen.width / 2 - img.width / 2
        y = screen.height * 4 / 5

        super().__init__(img, x, y, *args, **kwargs)
        self.scale = 1 / 2
        self.max_hp = 10**4
        self.current_hp = self.max_hp
        self.hp = 1

        self._screen = screen
        self._spawner = spawner
        self._base_y = y
        self._speed = 6
        self._max_laser_speed = 3
        self._pattern_pointer = 0
        self._pattern = [
            "SHOOT 1 / 5",
            "GOTO -90",
            "SHOOT 1 / 2",
            "GOTO 50% 10",
            "SHOOT 1 / 5",
            "GOTO 90",
            "SHOOT 1 / 1",
            "GOTO 50% 10",
        ]
        self.hitzone = pyglet.shapes.Rectangle(
            self.x,
            self.y,
            self.width,
            self.height,
            color=(255, 0, 0),
        )
        self.hitzone.opacity = 128

    def update(self, dt):
        current_pattern = self._pattern[self._pattern_pointer]
        target = self.read_pattern(current_pattern)

        direction = target - self.position
        # move is a fraction of the direction based on the direction, speed and dt
        move = direction.normalize() * dt * 40 * self._speed
        # if we are close enough to destination, next part of the pattern
        if direction.length_squared() <= move.length_squared():
            self._pattern_pointer = (self._pattern_pointer + 1) % len(self._pattern)
            return
        self.x += move.x
        self.y += move.y

        self.hitzone.x = self.x
        self.hitzone.y = self.y

    def hit(self):
        self.current_hp -= 1
        self.hp = self.current_hp / self.max_hp

        if self.current_hp <= 0:
            self.delete()

    def _pew_pew(self, dt):
        src = Vec2(self.x, self.y)
        tgt = Vec2(self.x, self.y - 1)
        speed = 2 + random() * self._max_laser_speed
        self._spawner.laser(src, tgt, speed=speed, color="lime")

    def read_pattern(self, pattern):
        match pattern.split():
            case ("SHOOT", a, "/", b):
                self._set_shoot_freq(int(a) / int(b))
                return Vec2(self.x, self.y)
            case ("SHOOT", "0"):
                self._set_shoot_freq(0)
                return Vec2(self.x, self.y)
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

    def _set_shoot_freq(self, freq):
        pyglet.clock.unschedule(self._pew_pew)
        if freq:
            pyglet.clock.schedule_interval(self._pew_pew, freq)
