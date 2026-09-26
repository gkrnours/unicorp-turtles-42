from random import randint

import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.boss import Boss
from unicorp_turtles_42.loader import colors, loader
from unicorp_turtles_42.spawner import Spawner


class Ship(pyglet.sprite.Sprite):
    def __init__(self, screen, spawner, *args, **kwargs):
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
        self.scale = 1 / 2
        self._direction = Vec2(0, 0)
        self._velocity = 40 * 6
        self._clone_count = 0

        self._clone_offset = [
            Vec2(120, -45),
            Vec2(-120, -45),
            Vec2(80, -145),
            Vec2(-80, -145),
        ]
        self._clones = []
        for i in self._clone_offset:
            s = pyglet.sprite.Sprite(*args, img=img, x=0, y=0, **kwargs)
            s.anchor_x = self.anchor_x
            s.anchor_y = self.anchor_y
            s.scale = self.scale
            s.opacity = 0
            self._clones.append(s)

        self._hitzone_offset = Vec2(
            self.anchor_x * self.scale,
            self.anchor_y * self.scale,
        )
        self.hitzone = pyglet.shapes.Ellipse(
            self.x + self._hitzone_offset.x,
            self.y + self._hitzone_offset.y,
            75 * self.scale,
            98 * self.scale,
            color=colors()["red"],
        )
        self.hitzone.opacity = 0x10

        self._spawner = spawner
        self._laser_source_left = Vec2(38, 180)
        self._laser_source_right = Vec2(201, 180)

    def set_direction(self, vector):
        self._direction = vector.normalize()

    def start_firing(self):
        pyglet.clock.schedule_interval(self.do_fire, 1 / 7)

    def stop_firing(self):
        pyglet.clock.unschedule(self.do_fire)

    def do_fire(self, dt):
        self._do_fire(Vec2(0, 0))
        for i in range(self._clone_count):
            self._do_fire(self._clone_offset[i])

    def _do_fire(self, o):
        jitter = randint(-6, 6)
        source = (
            o + self.position + self._laser_source_left * self.scale + Vec2(jitter, 0)
        )
        target = source + Vec2(0, 10)
        self._spawner.laser(source, target, color="pink", speed=10, tag="me")
        jitter = randint(-6, 6)
        source = (
            o + self.position + self._laser_source_right * self.scale + Vec2(jitter, 0)
        )
        target = source + Vec2(0, 10)
        self._spawner.laser(source, target, color="pink", speed=10, tag="me")

    def invoke(self):
        if len(self._clone_offset) <= self._clone_count:
            return
        self._clone_count += 1
        self._reset_clone_opacity()

    def revoke(self):
        if self._clone_count <= 0:
            return
        self._clone_count -= 1
        self._reset_clone_opacity()

    def _reset_clone_opacity(self):
        for i, c in enumerate(self._clones):
            c.opacity = 0x70 if i + 1 <= self._clone_count else 0

    def update(self, dt):
        new_pos = Vec2(self.x, self.y) + self._direction * self._velocity * dt
        self.x, self.y = new_pos
        self.hitzone.position = new_pos + self._hitzone_offset
        for c, o in zip(self._clones, self._clone_offset):
            c.x = self.x + o.x
            c.y = self.y + o.y


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
        self._boss = None
        self._mouse_pos = Vec2(self.width // 2, self.height // 2)

        self._build()

    def _build(self):
        batch = self._drawing_batch
        self._spawner = Spawner(self, batch)
        base_group = pyglet.graphics.Group(order=0)
        ship_group = pyglet.graphics.Group(order=1)

        self._ship = Ship(
            screen=self,
            spawner=self._spawner,
            batch=batch,
            group=ship_group,
        )
        self._boss = Boss(
            loader().image("gfx/boss.png"),
            x=0,
            y=0,
            screen=self,
            spawner=self._spawner,
            batch=batch,
            group=ship_group,
        )

        """
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
        """

    def _check_collision(self):
        if laser := self._spawner.do_collide(self._ship, "laser:other"):
            laser.stop()
            self.dispatch_event("on_hit")
        while laser := self._spawner.do_collide(self._boss, "laser:me"):
            laser.stop()
            self._boss.hit()
            self.dispatch_event("on_hit_boss", self._boss.hp)

    def draw(self):
        self._drawing_batch.draw()

    def update(self, dt):
        self._check_collision()
        self._spawner.update(dt)
        self._ship.update(dt)
        self._boss.update(dt)

    def move_mouse(self, dx, dy):
        self._mouse_pos += Vec2(dx, dy)
        self._ship.set_direction(Vec2(dx, dy))

    def set_direction(self, vector):
        self._ship.set_direction(vector)

    def start_firing(self):
        self._ship.start_firing()

    def stop_firing(self):
        self._ship.stop_firing()

    def invoke(self):
        self._ship.invoke()

    def revoke(self):
        self._ship.revoke()


PlayArea.register_event_type("on_hit")
PlayArea.register_event_type("on_hit_boss")
