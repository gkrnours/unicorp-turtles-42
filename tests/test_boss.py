from unittest.mock import MagicMock

from unicorp_turtles_42.boss import Boss
from unicorp_turtles_42.loader import loader


def dummy_screen():
    screen = MagicMock()
    screen.width = 800
    screen.height = 600
    return screen


def dummy_texture():
    tex = loader().image("gfx/icon_48.png")
    return tex


def boss():
    img = dummy_texture()
    screen = dummy_screen()
    b = Boss(img, 0, 0, screen=screen)

    return b


def test_boss():
    b = boss()

    assert 350 < b.x < 400
    assert 400 < b.y < 600


def test_read_pattern_1():
    b = boss()
    target = b.read_pattern("GOTO 10 10")

    assert b._speed == 10
    assert target.x == 10


def test_read_pattern_2():
    b = boss()
    target = b.read_pattern("GOTO -10")

    assert b._speed == 6
    assert target.x == 766  # (800 - (48 / 2) - 10)


def test_read_pattern_3():
    b = boss()
    target = b.read_pattern("GOTO 10% 12")

    assert b._speed == 12
    assert target.x == 80
