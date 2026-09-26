import itertools
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

        # debug statement
        if False:
            print(
                f"\robjects: {len(self._objects)}, dt: {sum(self._recent_dts) / 10:.4}",
                end="",
                flush=True,
            )
        for obj in self._objects:
            obj.update(dt)

    def do_collide(self, obj, *tags):
        for tag in tags:
            for item in self._tags[tag]:
                if obj in item:
                    return item

    @cached_property
    def laser_img(self, color=None):
        return loader().image("gfx/laser.png", rotate=90)

    def laser(self, origin, target, color="red", speed=1, tag="other", group=None):
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
        laser.rotation = -math.degrees(v.heading())
        laser.tag = tag
        laser.init_hit()
        self._objects.append(laser)
        self._tags[f"laser:{tag}"].append(laser)

        @laser.event
        def on_outofbound():
            laser.stop()

        @laser.event
        def on_remove():
            self._objects.remove(laser)
            self._tags[f"laser:{laser.tag}"].remove(laser)

        return laser


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, screen, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._screen = screen
        self._removed = False
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self._hits = None

    def init_hit(self):
        self._hitpoint = pyglet.math.Vec2(self.x, self.y)
        w, h = self._texture.width, self._texture.height
        self._hit_offset = pyglet.math.Vec2(
            +self.anchor_x / 2 + w * 2 / 3 - 2,
            -self.anchor_y / 2 - h * 1 / 3 + 2,
        )

    def __contains__(self, other):
        if self._removed:
            return False
        if isinstance(other, tuple):
            x, y = other
            if (
                self.x <= x <= self.x + self.width
                and self.y <= y <= self.y + self.height
            ):
                return True
        elif hitzone := getattr(other, "hitzone", None):
            return self._hitpoint in hitzone
        else:
            print(other)
            print("oops")

        return False

    def update(self, dt):
        if self._removed:
            return
        self.check_bounds()
        if self._removed:
            return
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        offset = pyglet.math.Vec2.from_heading(
            math.radians(-self.rotation) + self._hit_offset.heading(),
            self._hit_offset.length(),
        )
        self._hitpoint = self.position + offset

    def check_bounds(self):
        if self._removed:
            return
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = self._screen.width + self.image.width / 2
        max_y = self._screen.height + self.image.height / 2

        if self.x < min_x:
            self.dispatch_event("on_outofbound")
            return
        elif max_x < self.x:
            self.dispatch_event("on_outofbound")
            return
        if self.y < min_y:
            self.dispatch_event("on_outofbound")
            return
        elif max_y < self.y:
            self.dispatch_event("on_outofbound")
            return

    def stop(self):
        self._removed = True
        self.dispatch_event("on_remove")
        self.velocity_x, self.velocity_y = 0, 0
        self.visible = False
        self.x, self.y = 0, 0
        self.delete()


PhysicalObject.register_event_type("on_outofbound")
PhysicalObject.register_event_type("on_remove")
