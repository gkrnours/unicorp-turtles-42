import pyglet
from pyglet.window import key, mouse

from unicorp_turtles_42.input import InputManager
from unicorp_turtles_42.loader import loader


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(visible=False)
        self._decorate()

        input_manager = InputManager()
        input_manager

        self._drawing_batch = None
        self._turtle = None
        self._label = None
        self._eye_left = None
        self._eye_left_pos = None
        self._eye_right = None
        self._eye_right_pos = None
        self._build()

        self.set_visible()

    def _decorate(self):
        self.set_caption("Unicorp Turtles 42")
        icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
        self.set_icon(*icons)

    def _build(self):
        self._drawing_batch = batch = pyglet.graphics.Batch()
        base_group = pyglet.graphics.Group(order=0)
        front_group = pyglet.graphics.Group(order=1)

        image = loader().image("gfx/turtle.png")
        self._turtle = pyglet.sprite.Sprite(
            img=image,
            x=self.width // 2 - image.width // 2,
            y=self.height * 2 // 3 - image.height // 2,
            batch=batch,
            group=base_group,
        )
        self._label = pyglet.text.Label(
            "Turtle",
            font_size=36,
            x=self.width // 2,
            y=self._turtle.y,
            anchor_x="center",
            anchor_y="top",
            batch=batch,
            group=base_group,
        )
        eyes_config = {
            "radius": 5,
            "color": (0xFF, 0xFF, 0xFF),
            "batch": batch,
            "group": front_group,
        }
        self._eye_left_pos = pyglet.math.Vec2(
            self.width // 2 - 200 + 16,
            self.height * 2 // 3 - 20 + 12,
        )
        self._eye_left = pyglet.shapes.Circle(
            *self._eye_left_pos,
            **eyes_config,
        )
        self._eye_right_pos = pyglet.math.Vec2(
            self.width // 2 - 120 + 10,
            self.height * 2 // 3 - 20 + 10,
        )
        self._eye_right = pyglet.shapes.Circle(
            *self._eye_right_pos,
            **eyes_config,
        )

    # Events
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_CTRL:
            exit(0)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"click at {x:.0f}:{y:.0f}")

    def on_mouse_motion(self, x, y, dx, dy):
        eyes = [(-10, -12), (10, 12)]
        delta_left = pyglet.math.Vec2(x, y) - self._eye_left_pos
        delta_right = pyglet.math.Vec2(x, y) - self._eye_right_pos
        self._eye_left.position = self._eye_left_pos + (delta_left / 30).clamp(*eyes)
        self._eye_right.position = self._eye_right_pos + (delta_right / 30).clamp(*eyes)

    def on_draw(self):
        self.clear()
        self._drawing_batch.draw()


def run():
    window = MainWindow()
    window

    pyglet.app.run()


if __name__ == "__main__":
    run()
