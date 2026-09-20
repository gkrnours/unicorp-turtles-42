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

        self._turtle = None
        self._label = None
        self._build()

        self.set_visible()

    def _decorate(self):
        self.set_caption("Unicorp Turtles 42")
        icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
        self.set_icon(*icons)

    def _build(self):
        image = loader().image("gfx/turtle.png")
        self._turtle = pyglet.sprite.Sprite(
            img=image,
            x=self.width // 2 - image.width // 2,
            y=self.height * 2 // 3 - image.height // 2,
        )

        self._label = pyglet.text.Label(
            "Turtle",
            font_size=36,
            x=self.width // 2,
            y=self._turtle.y,
            anchor_x="center",
            anchor_y="top",
        )

    # Events
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_CTRL:
            exit(0)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"click at {x:.0f}:{y:.0f}")

    def on_draw(self):
        self.clear()
        self._turtle.draw()
        self._label.draw()


def run():
    window = MainWindow()
    window

    pyglet.app.run()


if __name__ == "__main__":
    run()
