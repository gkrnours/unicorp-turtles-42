import pyglet
from pyglet.window import key, mouse

from unicorp_turtles_42.game import PlayArea
from unicorp_turtles_42.gui import GUI
from unicorp_turtles_42.input import InputManager
from unicorp_turtles_42.loader import loader

MOVE_DELTAS = [
    ("UP", pyglet.math.Vec2(0, 1)),
    ("DOWN", pyglet.math.Vec2(0, -1)),
    ("LEFT", pyglet.math.Vec2(-1, 0)),
    ("RIGHT", pyglet.math.Vec2(1, 0)),
]


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(visible=False)

        self._decorate()
        self.set_exclusive_mouse()
        # self.set_fullscreen()

        if False:
            input_manager = InputManager()
            input_manager

        self._play_area = PlayArea(self)
        self._gui = GUI(self)
        self._dvec = pyglet.math.Vec2(0, 0)
        self._keys = {
            "UP": [key.W, key.UP],
            "DOWN": [key.S, key.DOWN],
            "LEFT": [key.A, key.LEFT],
            "RIGHT": [key.D, key.RIGHT],
            "FIRE": [key.SPACE],
        }

        self._play_area.push_handlers(self.on_hit)

        self.set_visible()

    def _decorate(self):
        self.set_caption("Unicorp Turtles 42")
        icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
        self.set_icon(*icons)

    def update(self, dt):
        self._play_area.update(dt)
        self._gui.update(dt)

    # Events
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_CTRL:
            exit(0)
        for k, delta in MOVE_DELTAS:
            if symbol in self._keys[k]:
                self._dvec += delta
        if symbol in self._keys["FIRE"]:
            self._play_area.start_firing()
        self._play_area.set_direction(self._dvec)

    def on_key_release(self, symbol, modifiers):
        for k, delta in MOVE_DELTAS:
            if symbol in self._keys[k]:
                self._dvec -= delta
        if symbol in self._keys["FIRE"]:
            self._play_area.stop_firing()
        self._play_area.set_direction(self._dvec)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"click at {x:.0f}:{y:.0f}")

    # mouse motion don't fire when mouse stop
    # def on_mouse_motion(self, x, y, dx, dy):
    #     self._play_area.move_mouse(dx, dy)

    def on_draw(self):
        self.clear()
        self._play_area.draw()
        self._gui.draw()

    def on_hit(self):
        self._gui.hit_count += 1
        print("got hit")


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
