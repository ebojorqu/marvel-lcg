import sys
from core import Unused

__all__ = ["World", "GAME_OVER"]


def _placeholder(name: str):
    return type(name, (), {"__module__": __name__})


def __getattr__(name):
    module = sys.modules.get("game.world.world")
    if module is not None:
        if name in module.__dict__:
            return getattr(module, name)
    if name == "World":
        if module is not None and hasattr(module, "World"):
            return module.World
        return _placeholder("World")
    if name == "GAME_OVER":
        if module is not None and hasattr(module, "GAME_OVER"):
            return module.GAME_OVER
        return False
    raise AttributeError(name)

Unused(__all__)

