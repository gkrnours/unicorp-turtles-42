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

        self._image = None
        self._image_pos = None
        self._label = None
        self._build()

        self.set_visible()

    def _decorate(self):
        self.set_caption("Unicorp Turtles 42")
        icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
        self.set_icon(*icons)

    def _build(self):
        self._image = loader().image("gfx/turtle.png")
        img_x = self.width // 2 - self._image.width // 2
        img_y = self.height * 2 // 3 - self._image.height // 2
        self._image_pos = (img_x, img_y)

        self._label = pyglet.text.Label(
            "Turtle",
            font_size=36,
            x=self.width // 2,
            y=img_y,
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
        self._image.blit(*self._image_pos)
        self._label.draw()


def run():
    window = MainWindow()
    window

    pyglet.app.run()


if __name__ == "__main__":
    run()
