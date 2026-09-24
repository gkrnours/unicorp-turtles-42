import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors, loader

BOX_COLORS = {
    "bottom": "navy",
    "middle": "cerulean",
    "top": "ochre",
}


def box(repeat, screen, batch, group):
    images_repeat = [
        (loader().image(f"gfx/UI-repeat-{part}.png"), BOX_COLORS[part])
        for part in ["bottom", "middle", "top"]
    ]
    images_end = [
        (loader().image(f"gfx/UI-end-{part}.png"), BOX_COLORS[part])
        for part in ["bottom", "middle", "top"]
    ]
    delta = images_repeat[0][0].width

    parts = []
    sprites_config = dict(
        batch=batch,
        group=group,
    )
    for i in range(repeat):
        for img, color in images_repeat:
            sprite = pyglet.sprite.Sprite(
                img=img,
                y=screen.height - img.height,
                x=0 + delta * i,
                **sprites_config,
            )
            sprite.color = colors()[color]
            parts.append(sprite)
    for img, color in images_end:
        sprite = pyglet.sprite.Sprite(
            img=img,
            y=screen.height - img.height,
            x=0 + delta * repeat,
            **sprites_config,
        )
        sprite.color = colors()[color]
        parts.append(sprite)

    return parts


class GUI(pyglet.event.EventDispatcher):
    def __init__(self, screen):
        self._screen = screen
        self.width = screen.width
        self.height = screen.height

        self._drawing_batch = None
        self._layers = None
        self._sprites = None
        self._fps = None

        self._build()

    def _build(self):
        self._drawing_batch = batch = pyglet.graphics.Batch()
        group = pyglet.graphics.Group(order=100)

        self._layers = box(1, self._screen, batch, group)

        self._fps = pyglet.window.FPSDisplay(self._screen)
        self._fps.label.anchor_y = "top"
        self._fps.label.x = 5
        self._fps.label.y = self.height
        self._fps.label.color = colors()["lilac"]

    def draw(self):
        self._drawing_batch.draw()
        self._fps.draw()

    def update(self, dt):
        pass
