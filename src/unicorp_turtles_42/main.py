import pyglet
from pyglet.window import key, mouse

from unicorp_turtles_42.input import InputManager
from unicorp_turtles_42.loader import loader


def run():
    window = pyglet.window.Window(
        caption="Unicorp Turtles 42",
        visible=False,
    )
    icons = [loader().image(f"gfx/icon_{size}.png") for size in (16, 32, 48)]
    window.set_icon(*icons)

    image = loader().image("gfx/turtle.png")
    img_x = window.width // 2 - image.width // 2
    img_y = window.height * 2 // 3 - image.height // 2
    label = pyglet.text.Label(
        "Turtle",
        font_size=36,
        x=window.width // 2,
        y=img_y,
        anchor_x="center",
        anchor_y="top",
    )

    input_manager = InputManager()
    input_manager

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_CTRL:
            exit(0)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            print(f"click at {x:.0f}:{y:.0f}")

    @window.event
    def on_draw():
        window.clear()
        image.blit(img_x, img_y)
        label.draw()

    window.set_visible()
    pyglet.app.run()


if __name__ == "__main__":
    run()
