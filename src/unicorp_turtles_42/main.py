import pyglet

from unicorp_turtles_42.loader import loader


def run():
    window = pyglet.window.Window()
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

    @window.event
    def on_draw():
        window.clear()
        image.blit(img_x, img_y)
        label.draw()

    pyglet.app.run()


if __name__ == "__main__":
    run()
