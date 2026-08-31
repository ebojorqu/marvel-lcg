import importlib
import sys
from core import Unused

__all__ = ["World", "GAME_OVER"]


def _placeholder(name: str):
    return type(name, (), {"__module__": __name__})


def __getattr__(name):
    module_name = "game.world.world"
    module = sys.modules.get(module_name)
    if module is None:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            module = None

    if module is not None:
        if name in module.__dict__:
            value = getattr(module, name)
            globals()[name] = value
            return value

    if name == "World":
        if module is not None and hasattr(module, "World"):
            value = module.World
            globals()[name] = value
            return value
        value = _placeholder("World")
        globals()[name] = value
        return value
    if name == "GAME_OVER":
        if module is not None and hasattr(module, "GAME_OVER"):
            value = module.GAME_OVER
            globals()[name] = value
            return value
        value = False
        globals()[name] = value
        return value
    raise AttributeError(name)

Unused(__all__)

