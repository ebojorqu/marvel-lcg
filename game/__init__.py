from importlib import import_module
from core import Unused

# Keep the package API stable for wildcard imports while still deferring heavy
# runtime imports until the names are actually requested.
__all__ = [
    "Game",
    "GameState",
    "GameSession",
    "NewGameDescriptor",
    "GameStatistics",
]


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

