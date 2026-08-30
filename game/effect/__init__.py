from core import Unused

__all__ = ["Effect"]


def __getattr__(name):
    if name == "Effect":
        from game.effect.effect import Effect
        return Effect
    raise AttributeError(name)

Unused(__all__)

