import math
from collections import defaultdict
from functools import cached_property

import pyglet

from unicorp_turtles_42.loader import colors, loader


class Spawner(pyglet.event.EventDispatcher):
    def __init__(self, screen, batch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._screen = screen
        self._batch = batch
        self._objects = []
        self._tags = defaultdict(list)
        self._recent_dts = [0] * 10

    def update(self, dt):
        self._recent_dts.append(dt)
        self._recent_dts.pop(0)

        print(
            f"\robjects: {len(self._objects)}, dt: {sum(self._recent_dts) / 10:.4}",
            end="",
            flush=True,
        )
        for obj in self._objects:
            obj.update(dt)

    def do_collide(self, pos, *tags):
        for tag in tags:
            for item in self._tags[tag]:
                if (
                    item.x <= pos.x <= item.x + item.width
                    and item.y <= pos.y <= item.y + item.height
                ):
                    return True

    @cached_property
    def laser_img(self, color=None):
        return loader().image("gfx/laser.png")

    def laser(self, origin, target, color="red", speed=1, group=None):
        if group is None:
            group = pyglet.graphics.Group(7)
        v = target - origin
        laser = PhysicalObject(
            screen=self._screen,
            img=self.laser_img,
            x=origin.x,
            y=origin.y,
            batch=self._batch,
            group=group,
        )
        laser.color = colors()[color]
        laser.anchor_x = self.laser_img.width // 2
        laser.anchor_y = self.laser_img.height // 2
        laser.velocity_x, laser.velocity_y = v.normalize() * 40 * speed
        laser.rotation = 90 - math.degrees(v.heading())
        self._objects.append(laser)
        self._tags["laser"].append(laser)

        @laser.event
        def on_outofbound():
            laser.stop()
            self._objects.remove(laser)
            self._tags["laser"].remove(laser)

        return laser


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._screen = screen
        self._move = True
        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.check_bounds()
        if not self._move:
            return
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = self._screen.width + self.image.width / 2
        max_y = self._screen.height + self.image.height / 2

        if self.x < min_x:
            self.dispatch_event("on_outofbound")
        elif max_x < self.x:
            self.dispatch_event("on_outofbound")
        if self.y < min_y:
            self.dispatch_event("on_outofbound")
        elif max_y < self.y:
            self.dispatch_event("on_outofbound")

    def stop(self):
        self._move = False
        self.velocity_x, self.velocity_y = 0, 0
        self.visible = False
        self.x, self.y = self._screen.x, self._screen.y
        self.delete()


PhysicalObject.register_event_type("on_outofbound")
