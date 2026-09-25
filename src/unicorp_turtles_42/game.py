from random import choice, randint, random

import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors, loader
from unicorp_turtles_42.spawner import Spawner


class Ship(pyglet.sprite.Sprite):
    def __init__(self, screen, *args, **kwargs):
        img = loader().image("gfx/ship.png")
        super().__init__(
            *args,
            img=img,
            x=screen.width // 2 - img.width // 2,
            y=screen.height // 2 - img.height // 2,
            **kwargs,
        )
        self.anchor_x = 128
        self.anchor_y = 129
        self._direction = Vec2(0, 0)
        self._velocity = 90

    def set_direction(self, vector):
        self._direction = vector.normalize()

    def update(self, dt):
        new_pos = Vec2(self.x, self.y) + self._direction * self._velocity * dt
        self.x, self.y = new_pos


class PlayArea(pyglet.event.EventDispatcher):
    def __init__(self, screen):
        self._max_speed = 6
        self._laser_volley = 1
        self._laser_cooldown = 1 / 10

        self._screen = screen
        self.width = screen.width
        self.height = screen.height

        self._spawner = None
        self._drawing_batch = pyglet.graphics.Batch()
        self._ship = None
        self._mouse_pos = Vec2(self.width // 2, self.height // 2)

        self._build()

    def _build(self):
        batch = self._drawing_batch
        self._spawner = Spawner(self, batch)
        base_group = pyglet.graphics.Group(order=0)
        ship_group = pyglet.graphics.Group(order=1)

        self._ship = Ship(
            screen=self,
            batch=batch,
            group=ship_group,
        )

        laser_source_circle_config = {
            "radius": 5,
            "color": colors()["white"],
            "batch": batch,
            "group": base_group,
        }
        laser_source_config = [
            (Vec2(30, 30), "red"),
            (Vec2(self.width - 30, 30), "green"),
            (Vec2(self.width - 30, self.height - 90), "gold"),
            (Vec2(30, self.height - 90), "cyan"),
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
        if self._spawner.do_collide(Vec2(self._ship.x, self._ship.y), "laser"):
            exit(0)

    def draw(self):
        self._drawing_batch.draw()

    def update(self, dt):
        self._check_collision()
        self._spawner.update(dt)
        self._ship.update(dt)

    def move_mouse(self, dx, dy):
        self._mouse_pos += Vec2(dx, dy)
        self._ship.set_direction(Vec2(dx, dy))

    def set_direction(self, vector):
        self._ship.set_direction(vector)
