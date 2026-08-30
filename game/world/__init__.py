from core import Unused

__all__ = ["World", "GAME_OVER"]


def __getattr__(name):
    if name == "World":
        from game.world.world import World
        return World
    if name == "GAME_OVER":
        from game.world.world import GAME_OVER
        return GAME_OVER
    raise AttributeError(name)

Unused(__all__)

