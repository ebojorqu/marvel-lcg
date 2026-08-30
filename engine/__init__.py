from core import Unused

__all__ = ["Engine"]


def __getattr__(name):
    if name == "Engine":
        from engine.engine import Engine
        return Engine
    raise AttributeError(name)


Unused(__all__)

