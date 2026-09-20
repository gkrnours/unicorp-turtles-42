from functools import cache
from pathlib import Path

import pyglet


@cache
def loader():
    return pyglet.resource.Loader(
        script_home=Path(__file__).parent,
    )
