import importlib
import sys
from core import Unused

__all__ = ["World", "GAME_OVER"]


def _placeholder(name: str):
    return type(name, (), {"__module__": __name__})


def _resolve_runtime_world():
    module_name = "game.world.world"
    module = sys.modules.get(module_name)
    if module is None:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            return None
    if hasattr(module, "World"):
        return module.World
    return None


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
        runtime = _resolve_runtime_world()
        if runtime is not None:
            globals()[name] = runtime
            return runtime
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


try:
    from game.world.world import World, GAME_OVER
except Exception:
    World = _placeholder("World")
    GAME_OVER = False
    runtime_world = _resolve_runtime_world()
    if runtime_world is not None:
        World = runtime_world

if isinstance(World, type):
    World.__module__ = "game.world.world"

globals()["World"] = World
globals()["GAME_OVER"] = GAME_OVER

Unused(__all__)

