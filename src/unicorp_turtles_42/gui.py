import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors, loader


class GUI(pyglet.event.EventDispatcher):
    def __init__(self, screen):
        self._screen = screen
        self.width = screen.width
        self.height = screen.height

        self._drawing_batch = None
        self._layers = None
        self._sprites = None

        self._build()

    def _build(self):
        self._drawing_batch = batch = pyglet.graphics.Batch()
        group = pyglet.graphics.Group(order=100)

        layer_images = [
            (loader().image(f"gfx/UI-end-{part}.png"), color)
            for part, color in [
                ("bottom", "navy"),
                ("middle", "cerulean"),
                ("top", "ochre"),
            ]
        ]

        self._layers = []
        for img, color in layer_images:
            sprite = pyglet.sprite.Sprite(
                img=img,
                x=0,
                y=self.height - img.height,
                batch=batch,
                group=group,
            )
            sprite.color = colors()[color]
            self._layers.append(sprite)

    def draw(self):
        self._drawing_batch.draw()

    def update(self, dt):
        pass
