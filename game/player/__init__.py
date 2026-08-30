from core import Unused

__all__ = [
    "User", "Player", "PlayerFlag", "Scenario", "PlayerFinder", "Form",
]


def __getattr__(name):
    if name == "User":
        from game.player.user import User
        return User
    if name == "Player":
        from game.player.player import Player
        return Player
    if name == "PlayerFlag":
        from game.player.element.player_flag import PlayerFlag
        return PlayerFlag
    if name == "Scenario":
        from game.player.scenario import Scenario
        return Scenario
    if name == "PlayerFinder":
        from game.player.player_finder import PlayerFinder
        return PlayerFinder
    if name == "Form":
        from game.player.form.form import Form
        return Form
    raise AttributeError(name)

Unused(__all__)

