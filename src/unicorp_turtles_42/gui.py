import pyglet
from pyglet.math import Vec2

from unicorp_turtles_42.loader import colors, loader

BOX_COLORS = {
    "bottom": "navy",
    "middle": "cerulean",
    "top": "ochre",
}
TOP_LEFT = "top_left"
TOP_RIGHT = "top_right"


def box(repeat, screen, *, batch, group, corner=None):
    if corner is None or corner == TOP_LEFT:
        h_flip = False
    if corner == TOP_RIGHT:
        h_flip = True
    images_repeat = [
        (loader().image(f"gfx/UI-repeat-{part}.png", flip_x=h_flip), BOX_COLORS[part])
        for part in ["bottom", "middle", "top"]
    ]
    images_end = [
        (loader().image(f"gfx/UI-end-{part}.png", flip_x=h_flip), BOX_COLORS[part])
        for part in ["bottom", "middle", "top"]
    ]
    delta = images_repeat[0][0].width
    origin_repeat = Vec2(0, screen.height - images_repeat[0][0].height)
    origin_end = Vec2(delta * repeat, screen.height - images_repeat[0][0].height)
    if corner == TOP_RIGHT:
        origin_repeat = Vec2(
            screen.width - delta * (repeat - 1),
            origin_repeat.y,
        )
        origin_end = Vec2(
            screen.width - delta * (repeat + 1),
            origin_end.y,
        )

    parts = []
    sprites_config = dict(
        batch=batch,
        group=group,
    )
    for i in range(repeat):
        for img, color in images_repeat:
            sprite = pyglet.sprite.Sprite(
                img=img,
                x=origin_repeat.x + delta * i,
                y=origin_repeat.y,
                **sprites_config,
            )
            sprite.color = colors()[color]
            parts.append(sprite)
    for img, color in images_end:
        sprite = pyglet.sprite.Sprite(
            img=img,
            x=origin_end.x + delta * repeat,
            y=origin_end.y,
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

        self._layers = box(1, self._screen, corner=TOP_RIGHT, batch=batch, group=group)

        self._fps = pyglet.window.FPSDisplay(self._screen)
        self._fps.label.anchor_x = "right"
        self._fps.label.anchor_y = "top"
        self._fps.label.x = self._screen.width - 10
        self._fps.label.y = self.height
        self._fps.label.color = colors()["lilac"]

    def draw(self):
        self._drawing_batch.draw()
        self._fps.draw()

    def update(self, dt):
        pass
