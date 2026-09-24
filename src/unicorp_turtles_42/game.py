from random import choice, randint, random

import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors
from unicorp_turtles_42.spawner import Spawner


class PlayArea(pyglet.event.EventDispatcher):
    def __init__(self, screen):
        self._max_speed = 5
        self._laser_volley = 1
        self._laser_cooldown = 1 / 20

        self._screen = screen
        self.width = screen.width
        self.height = screen.height

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

    def _build(self):
        self._drawing_batch = batch = pyglet.graphics.Batch()
        self._spawner = Spawner(self, batch)
        base_group = pyglet.graphics.Group(order=0)
        front_group = pyglet.graphics.Group(order=1)

        laser_source_circle_config = {
            "radius": 5,
            "color": colors()["white"],
            "batch": batch,
            "group": base_group,
        }
        laser_source_config = [
            (Vec2(30, 30), "red"),
            (Vec2(self.width - 30, 30), "green"),
            (Vec2(self.width - 30, self.height - 30), "gold"),
            (Vec2(30, self.height - 30), "cyan"),
        ]
        self._laser_source = [
            pyglet.shapes.Circle(*pos, **laser_source_circle_config)
            for pos, _c in laser_source_config
        ]

        def pew_pew():
            s, c = choice(laser_source_config)
            t = Vec2(randint(0, self.width), randint(0, self.height))
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
