from __future__ import annotations

from core import *
from core import Unused

__all__ = [name for name in globals() if not name.startswith("_")]


def __getattr__(name):
    if name in {"AbilitiesType", "CardType", "CardTypeMin", "EventType", "PlayerType"}:
        from game.ability.condition import Condition
        mapping = {
            "AbilitiesType": "ABILITY_TYPE",
            "CardType": "CARD_TYPE",
            "CardTypeMin": "CARD_TYPE_MIN",
            "EventType": "EVENT_TYPE",
            "PlayerType": "PLAYER_TYPE",
        }
        return getattr(Condition, mapping[name])
    if name == "AbilityFactory":
        from game.ability.factory.ability_factory import AbilityFactory
        return AbilityFactory
    raise AttributeError(name)


Unused(__all__)
