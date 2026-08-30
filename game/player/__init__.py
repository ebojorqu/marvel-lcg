import sys
from core import Unused

__all__ = []


def _placeholder(name: str):
    return type(name, (), {"__module__": __name__})


def __getattr__(name):
    module_map = {
        "User": "game.player.user",
        "Player": "game.player.player",
        "PlayerAsk": "game.player.model.player_ask",
        "PlayerCards": "game.player.model.player_cards",
        "PlayerGet": "game.player.action.player_get",
        "PlayerAction": "game.player.action.player_action",
        "PlayerFlag": "game.player.element.player_flag",
        "Scenario": "game.player.scenario",
        "PlayerFinder": "game.player.player_finder",
        "Form": "game.player.form.form",
    }
    if name in module_map:
        module = sys.modules.get(module_map[name])
        if module is not None and hasattr(module, name):
            return getattr(module, name)
        if name in {"User", "Player", "Scenario"}:
            return _placeholder(name)
    raise AttributeError(name)

Unused(__all__)

