from functools import cache
from pathlib import Path

import pyglet


@cache
def loader():
    return pyglet.resource.Loader(
        script_home=Path(__file__).parent,
    )


@cache
def colors():
    catalog = {}
    with open(Path(__file__).parent / "rgb.txt") as f:
        for ln in f:
            if not ln or ln.startswith("#"):
                continue
            name, color = ln.rsplit(maxsplit=1)
            catalog[name] = (
                int(color[1:3], base=16),
                int(color[3:5], base=16),
                int(color[5:7], base=16),
            )
    return catalog
