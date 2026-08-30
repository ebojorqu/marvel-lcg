from __future__ import annotations

import sys

__all__ = [
    "EncounterCard", "EncounterNonVillainCard", "PlayerCard", "ClassCard",
    "Asset2", "Scheme2", "SchemeSide2", "Unit2", "Enemy", "Friend", "Villain",
]


_RESOLVED_CACHE: dict[str, object] = {}


def __getattr__(name):
    if name in _RESOLVED_CACHE:
        return _RESOLVED_CACHE[name]
    mapping = {
        "EncounterCard": "game.card.face.base.card_encounter:EncounterCard",
        "EncounterNonVillainCard": "game.card.face.base.card_encounter:EncounterNonVillainCard",
        "PlayerCard": "game.card.face.base.card_player:PlayerCard",
        "ClassCard": "game.card.face.base.card_player:ClassCard",
        "Asset2": "game.card.face.base.asset:Asset2",
        "Scheme2": "game.card.face.base.scheme:Scheme2",
        "SchemeSide2": "game.card.face.base.scheme_side:SchemeSide2",
        "Unit2": "game.card.face.base.unit:Unit2",
        "Enemy": "game.card.face.base.enemy:Enemy",
        "Friend": "game.card.face.base.friend:Friend",
        "Villain": "game.card.face.base.villain:Villain",
    }
    if name not in mapping:
        raise AttributeError(name)
    module_name, attr_name = mapping[name].split(":")
    module = __import__(module_name, fromlist=[attr_name])
    value = getattr(module, attr_name)
    _RESOLVED_CACHE[name] = value
    globals()[name] = value
    return value

