import pyglet
from pyglet.window import key, mouse

from unicorp_turtles_42.game import PlayArea
from unicorp_turtles_42.input import InputManager
from unicorp_turtles_42.loader import loader


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(visible=False)

        self._decorate()

        input_manager = InputManager()
        input_manager

        self._play_area = PlayArea(self)

        self.set_visible()

    def _decorate(self):
        self.set_caption("Unicorp Turtles 42")
        icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
        self.set_icon(*icons)

    def update(self, dt):
        self._play_area.update(dt)

    # Events
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_CTRL:
            exit(0)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"click at {x:.0f}:{y:.0f}")

    def on_mouse_enter(self, x, y):
        self._play_area.set_mouse(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        self._play_area.set_mouse(x, y)

    def on_draw(self):
        self.clear()
        self._play_area.draw()


def run():
    window = MainWindow()
    window

    pyglet.clock.schedule_interval(window.update, 1 / 120.0)
    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        print("bye~")


if __name__ == "__main__":
    run()
