from __future__ import annotations

import sys

from core import Unused

__all__ = [
    "CardFace", "CardFinder", "CardFinder2", "CardFinderHelper", "Deck2",
    "PowerProperty", "HasAttribute",
    "AttackProperty", "DefenseProperty", "RecoverProperty", "SchemeProperty", "ThwartProperty",
    "CanPlaceCounter", "CanPlaceToken",
    "CanAttacked", "HasAccelerationIcon", "CanAccelerationToken", "CanAttach", "HasAmplify", "HasAttack",
    "CanAttack", "CanBoost", "CanCrisis", "HasDefense", "CanDefense", "HasHazard", "CanHealth",
    "CanHinder", "CanIncite", "HasRecover", "CanRecover", "CanRetaliate", "HasScheme", "CanScheme",
    "CanSurge", "HasThwart", "CanThwart", "HasVictory", "HasSetup", "HasStarting", "HasUses",
    "HasHandSize", "HasModify", "HasStage", "HasBoostIcon", "HasCost", "HasAssault", "HasForm",
    "HasRestricted", "HasResourceIcon", "HasPermanent", "HasTemporary", "HasTeamUp", "CanTeamwork",
    "HasAlliance", "CanQuickstrike", "HasGuard", "HasPatrol", "HasVillainous", "HasMaxPer",
    "HasVulnerable", "HasToughness", "HasSteady", "HasStalwart", "CanStatus", "CanNoStatus",
    "HasPeril",
    "EncounterCard", "EncounterNonVillainCard", "PlayerCard", "ClassCard",
    "Asset2", "Scheme2", "SchemeSide2", "Unit2", "Enemy", "Friend", "Villain",
    "FinalType",
    "StatusCard", "Insert", "Challenge", "Ally", "Identity", "Hero", "AlterEgo", "Minion",
    "EncounterVillain", "Leader", "EncounterSideScheme", "MainScheme", "PlayerSideScheme",
    "Environment", "Upgrade", "Support", "Attachment", "Event", "Obligation", "Treachery",
    "Resource", "Evidence",
]


from core.meta_class.class_name import ClassNameMeta

_RESOLVED_CACHE: dict[str, object] = {}
_PLACEHOLDER_CACHE: dict[str, type] = {}


class _PlaceholderMeta(ClassNameMeta):
    pass


def _placeholder(name: str):
    if name in _PLACEHOLDER_CACHE:
        return _PLACEHOLDER_CACHE[name]
    placeholder = _PlaceholderMeta(name, (), {"__module__": __name__})
    _PLACEHOLDER_CACHE[name] = placeholder
    globals()[name] = placeholder
    return placeholder


def __getattr__(name):
    if name in globals():
        return globals()[name]
    if name in _RESOLVED_CACHE:
        return _RESOLVED_CACHE[name]
    if name in _PLACEHOLDER_CACHE:
        return _PLACEHOLDER_CACHE[name]

    if name == "CardFace":
        from game.card.face.card_face import CardFace
        _RESOLVED_CACHE[name] = CardFace
        globals()[name] = CardFace
        return CardFace

    if name in {"CardFinder", "CardFinder2"}:
        from game.card.card_finder.finder import CardFinder, CardFinder2
        value = CardFinder if name == "CardFinder" else CardFinder2
        _RESOLVED_CACHE[name] = value
        globals()[name] = value
        return value
    if name == "CardFinderHelper":
        from game.card.card_finder.helper import CardFinderHelper
        _RESOLVED_CACHE[name] = CardFinderHelper
        globals()[name] = CardFinderHelper
        return CardFinderHelper
    if name == "Deck2":
        from game.deck.deck import Deck2
        _RESOLVED_CACHE[name] = Deck2
        globals()[name] = Deck2
        return Deck2
    if name == "PowerProperty":
        from game.card.face.attribute.power.power_property import PowerProperty
        _RESOLVED_CACHE[name] = PowerProperty
        globals()[name] = PowerProperty
        return PowerProperty
    if name == "HasAttribute":
        from game.card.face.attribute.has_attribute import HasAttribute
        _RESOLVED_CACHE[name] = HasAttribute
        globals()[name] = HasAttribute
        return HasAttribute

    if name in {"AttackProperty", "DefenseProperty", "RecoverProperty", "SchemeProperty", "ThwartProperty"}:
        if name == "AttackProperty":
            from game.card.face.attribute.can_attack import AttackProperty
            value = AttackProperty
        elif name == "DefenseProperty":
            from game.card.face.attribute.can_defense import DefenseProperty
            value = DefenseProperty
        elif name == "RecoverProperty":
            from game.card.face.attribute.can_recover import RecoverProperty
            value = RecoverProperty
        elif name == "SchemeProperty":
            from game.card.face.attribute.can_scheme import SchemeProperty
            value = SchemeProperty
        else:
            from game.card.face.attribute.can_thwart import ThwartProperty
            value = ThwartProperty
        _RESOLVED_CACHE[name] = value
        globals()[name] = value
        return value

    if name in {"CanPlaceCounter", "CanPlaceToken"}:
        if name == "CanPlaceCounter":
            from game.card.face.attribute.can_place_counter import CanPlaceCounter
            value = CanPlaceCounter
        else:
            from game.card.face.attribute.can_place_token import CanPlaceToken
            value = CanPlaceToken
        _RESOLVED_CACHE[name] = value
        globals()[name] = value
        return value

    mapping = {
        "CanAttacked": "game.card.face.attribute.can_attacked:CanAttacked",
        "HasAccelerationIcon": "game.card.face.attribute.has_acceleration_icon:HasAccelerationIcon",
        "CanAccelerationToken": "game.card.face.attribute.can_acceleration_token:CanAccelerationToken",
        "CanAttach": "game.card.face.attribute.can_attach:CanAttach",
        "HasAmplify": "game.card.face.attribute.has_amplify:HasAmplify",
        "HasAttack": "game.card.face.attribute.can_attack:HasAttack",
        "CanAttack": "game.card.face.attribute.can_attack:CanAttack",
        "CanBoost": "game.card.face.attribute.can_boost:CanBoost",
        "CanCrisis": "game.card.face.attribute.has_crisis:CanCrisis",
        "HasDefense": "game.card.face.attribute.can_defense:HasDefense",
        "CanDefense": "game.card.face.attribute.can_defense:CanDefense",
        "HasHazard": "game.card.face.attribute.has_hazard:HasHazard",
        "CanHealth": "game.card.face.attribute.can_health:CanHealth",
        "CanHinder": "game.card.face.attribute.can_hinder:CanHinder",
        "CanIncite": "game.card.face.attribute.can_incite:CanIncite",
        "HasRecover": "game.card.face.attribute.can_recover:HasRecover",
        "CanRecover": "game.card.face.attribute.can_recover:CanRecover",
        "CanRetaliate": "game.card.face.attribute.can_retaliate:CanRetaliate",
        "HasScheme": "game.card.face.attribute.can_scheme:HasScheme",
        "CanScheme": "game.card.face.attribute.can_scheme:CanScheme",
        "CanSurge": "game.card.face.attribute.can_surge:CanSurge",
        "HasThwart": "game.card.face.attribute.can_thwart:HasThwart",
        "CanThwart": "game.card.face.attribute.can_thwart:CanThwart",
        "HasVictory": "game.card.face.attribute.has_victory:HasVictory",
        "HasSetup": "game.card.face.attribute.has_setup:HasSetup",
        "HasStarting": "game.card.face.attribute.has_starting:HasStarting",
        "HasUses": "game.card.face.attribute.has_uses:HasUses",
        "HasHandSize": "game.card.face.attribute.has_hand_size:HasHandSize",
        "HasModify": "game.card.face.attribute.has_modify:HasModify",
        "HasStage": "game.card.face.attribute.has_stage:HasStage",
        "HasBoostIcon": "game.card.face.attribute.has_boost_icon:HasBoostIcon",
        "HasCost": "game.card.face.attribute.has_cost:HasCost",
        "HasAssault": "game.card.face.attribute.has_assault:HasAssault",
        "HasForm": "game.card.face.attribute.has_form:HasForm",
        "HasRestricted": "game.card.face.attribute.has_restricted:HasRestricted",
        "HasResourceIcon": "game.card.face.attribute.has_resources:HasResourceIcon",
        "HasPermanent": "game.card.face.attribute.has_permanent:HasPermanent",
        "HasTemporary": "game.card.face.attribute.has_temporary:HasTemporary",
        "HasTeamUp": "game.card.face.attribute.has_teamup:HasTeamUp",
        "CanTeamwork": "game.card.face.attribute.can_teamwork:CanTeamwork",
        "HasAlliance": "game.card.face.attribute.has_alliance:HasAlliance",
        "CanQuickstrike": "game.card.face.attribute.can_quickstrike:CanQuickstrike",
        "HasGuard": "game.card.face.attribute.has_guard:HasGuard",
        "HasPatrol": "game.card.face.attribute.has_patrol:HasPatrol",
        "HasVillainous": "game.card.face.attribute.has_villainous:HasVillainous",
        "HasMaxPer": "game.card.face.attribute.has_max_per:HasMaxPer",
        "HasVulnerable": "game.card.face.attribute.has_vulnerable:HasVulnerable",
        "HasToughness": "game.card.face.attribute.has_toughness:HasToughness",
        "HasSteady": "game.card.face.attribute.has_steady:HasSteady",
        "HasStalwart": "game.card.face.attribute.has_stalwart:HasStalwart",
        "CanStatus": "game.card.face.attribute.can_status:CanStatus",
        "CanNoStatus": "game.card.face.attribute.can_status:CanNoStatus",
        "HasPeril": "game.card.face.attribute.has_peril:HasPeril",
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
        "FinalType": "game.card.face.base.final_type:FinalType",
        "StatusCard": "game.card.face.card_type.card_status:StatusCard",
        "Insert": "game.card.face.card_type.insert:Insert",
        "Challenge": "game.card.face.card_type.insert:Challenge",
        "Ally": "game.card.face.card_type.ally:Ally",
        "Identity": "game.card.face.card_type.identity:Identity",
        "Hero": "game.card.face.card_type.identity:Hero",
        "AlterEgo": "game.card.face.card_type.identity:AlterEgo",
        "Minion": "game.card.face.card_type.minion:Minion",
        "EncounterVillain": "game.card.face.card_type.villain:EncounterVillain",
        "Leader": "game.card.face.card_type.leader:Leader",
        "EncounterSideScheme": "game.card.face.card_type.scheme_side:EncounterSideScheme",
        "MainScheme": "game.card.face.card_type.scheme_main:MainScheme",
        "PlayerSideScheme": "game.card.face.card_type.scheme_player:PlayerSideScheme",
        "Environment": "game.card.face.card_type.environment:Environment",
        "Upgrade": "game.card.face.card_type.upgrade:Upgrade",
        "Support": "game.card.face.card_type.support:Support",
        "Attachment": "game.card.face.card_type.attachment:Attachment",
        "Event": "game.card.face.card_type.event:Event",
        "Obligation": "game.card.face.card_type.obligation:Obligation",
        "Treachery": "game.card.face.card_type.treachery:Treachery",
        "Resource": "game.card.face.card_type.resource:Resource",
        "Evidence": "game.card.face.card_type.evidence:Evidence",
    }

    if name not in mapping:
        raise AttributeError(name)

    module_name, attr_name = mapping[name].split(":")
    module = sys.modules.get(module_name)
    if module is None:
        try:
            __import__(module_name, fromlist=[attr_name])
        except Exception:
            return _placeholder(name)
        module = sys.modules.get(module_name)
    if module is None:
        return _placeholder(name)
    try:
        value = getattr(module, attr_name)
    except AttributeError:
        return _placeholder(name)
    _RESOLVED_CACHE[name] = value
    globals()[name] = value
    return value

Unused(__all__)

