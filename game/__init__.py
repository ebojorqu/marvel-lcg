from importlib import import_module
from core import Unused

# Avoid importing the full game runtime at package import time.
# Some modules import `game.*` packages while the package graph is still being
# initialized, which creates circular import loops. Import the runtime entry
# points lazily from the actual module that needs them instead.
# Keep wildcard imports empty so they do not inject placeholder runtime classes
# during partial bootstrapping.
__all__ = []


def __getattr__(name):
    mapping = {
        "Game": "game.game",
        "GameState": "game.game_run.game_state",
        "GameSession": "game.game_run.game_session",
        "NewGameDescriptor": "game.game_run.game_new",
        "GameStatistics": "game.statistics.game_statistics",
    }
    if name in mapping:
        module = import_module(mapping[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


Unused(__name__)
Unused(__all__)

