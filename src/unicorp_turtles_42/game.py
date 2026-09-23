from random import choice, randint, random

import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors, loader
from unicorp_turtles_42.spawner import Spawner


class PlayArea(pyglet.event.EventDispatcher):
    def __init__(self, screen):
        self._max_speed = 5
        self._laser_volley = 1
        self._laser_cooldown = 1 / 20

        self._screen = screen
        self.width = screen.width
        self.height = screen.height - 30
        self.x = 0
        self.y = 30

        self._spawner = None
        self._drawing_batch = None
        self._turtle = None
        self._label = None
        self._eye_left = None
        self._eye_left_pos = None
        self._eye_right = None
        self._eye_right_pos = None
        self._mouse_pos = Vec2(-1, -1)

        self._build()

    def lvec2(self, x, y):
        if x < 0:
            x = self.width + x
        if y < 0:
            y = self.height + y
        return Vec2(self.x + x, self.y + y)

    def _build(self):
        self._drawing_batch = batch = pyglet.graphics.Batch()
        self._spawner = Spawner(self, batch)
        base_group = pyglet.graphics.Group(order=0)
        front_group = pyglet.graphics.Group(order=1)

        laser_source_circle_config = {
            "radius": 5,
            "color": (0xFF, 0xFF, 0xFF),
            "batch": batch,
            "group": base_group,
        }
        laser_source_config = [
            (self.lvec2(30, 30), "red"),
            (self.lvec2(-30, 30), "green"),
            (self.lvec2(-30, -30), "gold"),
            (self.lvec2(30, -30), "cyan"),
        ]
        self._laser_source = [
            pyglet.shapes.Circle(*pos, **laser_source_circle_config)
            for pos, _c in laser_source_config
        ]

        def pew_pew():
            s, c = choice(laser_source_config)
            t = self.lvec2(randint(0, self.width), randint(0, self.height))
            self._spawner.laser(s, t, speed=1 + random() * self._max_speed, color=c)

        def do_pew_pew(dt):
            for i in range(self._laser_volley):
                pew_pew()

        pyglet.clock.schedule_interval(do_pew_pew, self._laser_cooldown)
        pew_pew()

    def _check_collision(self):
        if self._spawner.do_collide(self._mouse_pos, "laser"):
            exit(0)

    def draw(self):
        self._drawing_batch.draw()

    def update(self, dt):
        self._check_collision()
        self._spawner.update(dt)

    def set_mouse(self, x, y):
        self._mouse_pos = Vec2(x, y)
