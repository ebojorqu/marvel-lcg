from __future__ import annotations

from typing import TYPE_CHECKING

from core import *
from game.card.face.card_face import CardFace

from game.ability.factory import AbilityFactory
Unused(AbilityFactory)

__all__ = [
    "CardFace",
    "DamageProperty",
    "PowerProperty",
    "HasAttribute",
    "CanPlaceCounter",
    "CanPlaceToken",
    "CanAttacked",
    "HasAccelerationIcon",
    "CanAccelerationToken",
    "CanAttach",
    "HasAmplify",
    "HasAttack",
    "CanAttack",
    "CanBoost",
    "CanCrisis",
    "HasDefense",
    "CanDefense",
    "HasHazard",
    "CanHealth",
    "CanHinder",
    "CanIncite",
    "HasRecover",
    "CanRecover",
    "CanRetaliate",
    "HasScheme",
    "CanScheme",
    "CanSurge",
    "HasThwart",
    "CanThwart",
    "HasVictory",
    "HasSetup",
    "HasStarting",
    "HasUses",
    "HasHandSize",
    "HasModify",
    "HasStage",
    "HasBoostIcon",
    "HasCost",
    "HasAssault",
    "HasForm",
    "HasRestricted",
    "HasResourceIcon",
    "HasPermanent",
    "HasTemporary",
    "HasTeamUp",
    "CanTeamwork",
    "HasAlliance",
    "CanQuickstrike",
    "HasGuard",
    "HasPatrol",
    "HasVillainous",
    "HasMaxPer",
    "HasVulnerable",
    "HasToughness",
    "HasSteady",
    "HasStalwart",
    "CanStatus",
    "CanNoStatus",
    "HasPeril",
    "AbilityFactory",
]


def __getattr__(name):
    module_map = {
        "CardFace": "game.card.face.card_face",
        "DamageProperty": "game.element.damage_property",
        "PowerProperty": "game.card.face.attribute.power.power_property",
        "HasAttribute": "game.card.face.attribute.has_attribute",
        "CanPlaceCounter": "game.card.face.attribute.can_place_counter",
        "CanPlaceToken": "game.card.face.attribute.can_place_token",
        "CanAttacked": "game.card.face.attribute.can_attacked",
        "HasAccelerationIcon": "game.card.face.attribute.has_acceleration_icon",
        "CanAccelerationToken": "game.card.face.attribute.can_acceleration_token",
        "CanAttach": "game.card.face.attribute.can_attach",
        "HasAmplify": "game.card.face.attribute.has_amplify",
        "HasAttack": "game.card.face.attribute.can_attack",
        "CanAttack": "game.card.face.attribute.can_attack",
        "CanBoost": "game.card.face.attribute.can_boost",
        "CanCrisis": "game.card.face.attribute.has_crisis",
        "HasDefense": "game.card.face.attribute.can_defense",
        "CanDefense": "game.card.face.attribute.can_defense",
        "HasHazard": "game.card.face.attribute.has_hazard",
        "CanHealth": "game.card.face.attribute.can_health",
        "CanHinder": "game.card.face.attribute.can_hinder",
        "CanIncite": "game.card.face.attribute.can_incite",
        "HasRecover": "game.card.face.attribute.can_recover",
        "CanRecover": "game.card.face.attribute.can_recover",
        "CanRetaliate": "game.card.face.attribute.can_retaliate",
        "HasScheme": "game.card.face.attribute.can_scheme",
        "CanScheme": "game.card.face.attribute.can_scheme",
        "CanSurge": "game.card.face.attribute.can_surge",
        "HasThwart": "game.card.face.attribute.can_thwart",
        "CanThwart": "game.card.face.attribute.can_thwart",
        "HasVictory": "game.card.face.attribute.has_victory",
        "HasSetup": "game.card.face.attribute.has_setup",
        "HasStarting": "game.card.face.attribute.has_starting",
        "HasUses": "game.card.face.attribute.has_uses",
        "HasHandSize": "game.card.face.attribute.has_hand_size",
        "HasModify": "game.card.face.attribute.has_modify",
        "HasStage": "game.card.face.attribute.has_stage",
        "HasBoostIcon": "game.card.face.attribute.has_boost_icon",
        "HasCost": "game.card.face.attribute.has_cost",
        "HasAssault": "game.card.face.attribute.has_assault",
        "HasForm": "game.card.face.attribute.has_form",
        "HasRestricted": "game.card.face.attribute.has_restricted",
        "HasResourceIcon": "game.card.face.attribute.has_resources",
        "HasPermanent": "game.card.face.attribute.has_permanent",
        "HasTemporary": "game.card.face.attribute.has_temporary",
        "HasTeamUp": "game.card.face.attribute.has_teamup",
        "CanTeamwork": "game.card.face.attribute.can_teamwork",
        "HasAlliance": "game.card.face.attribute.has_alliance",
        "CanQuickstrike": "game.card.face.attribute.can_quickstrike",
        "HasGuard": "game.card.face.attribute.has_guard",
        "HasPatrol": "game.card.face.attribute.has_patrol",
        "HasVillainous": "game.card.face.attribute.has_villainous",
        "HasMaxPer": "game.card.face.attribute.has_max_per",
        "HasVulnerable": "game.card.face.attribute.has_vulnerable",
        "HasToughness": "game.card.face.attribute.has_toughness",
        "HasSteady": "game.card.face.attribute.has_steady",
        "HasStalwart": "game.card.face.attribute.has_stalwart",
        "CanStatus": "game.card.face.attribute.can_status",
        "CanNoStatus": "game.card.face.attribute.can_status",
        "HasPeril": "game.card.face.attribute.has_peril",
        "AbilityFactory": "game.ability.factory.ability_factory",
    }
    if name in module_map:
        module = __import__(module_map[name], fromlist=[name])
        value = getattr(module, name)
        globals()[name] = value
        return value
    raise AttributeError(name)


if TYPE_CHECKING:
    from game.ability import Ability
    from game.ability.factory import AbilityFactory
    from game.effect import Effect
    from game.message import Message
    from game.deck import Deck
    from game.player import Player
    from game.world.game_area import GameArea

from cards.paper import Paper

from game.element.damage_property import DamageProperty
from game.card.face.attribute.power.power_property import PowerProperty
from game.card.face.attribute.has_attribute import HasAttribute
from game.card.face.attribute.can_place_counter import CanPlaceCounter
from game.card.face.attribute.can_place_token import CanPlaceToken
from game.card.face.attribute.can_attacked import CanAttacked
from game.card.face.attribute.has_acceleration_icon import HasAccelerationIcon
from game.card.face.attribute.can_acceleration_token import CanAccelerationToken
from game.card.face.attribute.can_attach import CanAttach
from game.card.face.attribute.has_amplify import HasAmplify
from game.card.face.attribute.can_attack import HasAttack
from game.card.face.attribute.can_attack import CanAttack
from game.card.face.attribute.can_boost import CanBoost
from game.card.face.attribute.has_crisis import CanCrisis
from game.card.face.attribute.can_defense import HasDefense
from game.card.face.attribute.can_defense import CanDefense
from game.card.face.attribute.has_hazard import HasHazard
from game.card.face.attribute.can_health import CanHealth
from game.card.face.attribute.can_hinder import CanHinder
from game.card.face.attribute.can_incite import CanIncite
from game.card.face.attribute.can_recover import HasRecover
from game.card.face.attribute.can_recover import CanRecover
from game.card.face.attribute.can_retaliate import CanRetaliate
from game.card.face.attribute.can_scheme import HasScheme
from game.card.face.attribute.can_scheme import CanScheme
from game.card.face.attribute.can_surge import CanSurge
from game.card.face.attribute.can_thwart import HasThwart
from game.card.face.attribute.can_thwart import CanThwart
from game.card.face.attribute.has_victory import HasVictory
from game.card.face.attribute.has_setup import HasSetup
from game.card.face.attribute.has_starting import HasStarting
from game.card.face.attribute.has_uses import HasUses
from game.card.face.attribute.has_hand_size import HasHandSize
from game.card.face.attribute.has_modify import HasModify
from game.card.face.attribute.has_stage import HasStage
from game.card.face.attribute.has_boost_icon import HasBoostIcon
from game.card.face.attribute.has_cost import HasCost
from game.card.face.attribute.has_assault import HasAssault
from game.card.face.attribute.has_form import HasForm
from game.card.face.attribute.has_restricted import HasRestricted
from game.card.face.attribute.has_resources import HasResourceIcon
from game.card.face.attribute.has_permanent import HasPermanent
from game.card.face.attribute.has_temporary import HasTemporary
from game.card.face.attribute.has_teamup import HasTeamUp
from game.card.face.attribute.can_teamwork import CanTeamwork
from game.card.face.attribute.has_alliance import HasAlliance
from game.card.face.attribute.can_quickstrike import CanQuickstrike
from game.card.face.attribute.has_guard import HasGuard
from game.card.face.attribute.has_patrol import HasPatrol
from game.card.face.attribute.has_villainous import HasVillainous
from game.card.face.attribute.has_max_per import HasMaxPer
from game.card.face.attribute.has_vulnerable import HasVulnerable
from game.card.face.attribute.has_toughness import HasToughness
from game.card.face.attribute.has_steady import HasSteady
from game.card.face.attribute.has_stalwart import HasStalwart
from game.card.face.attribute.can_status import CanStatus, CanNoStatus
from game.card.face.attribute.has_peril import HasPeril

# Ensure the package namespace exposes the real classes, not the bootstrap placeholder
# objects injected by `core` during early import-time resolution.
_REAL_CLASS_EXPORTS = {
    "CardFace": "game.card.face.card_face",
    "DamageProperty": "game.element.damage_property",
    "PowerProperty": "game.card.face.attribute.power.power_property",
    "HasAttribute": "game.card.face.attribute.has_attribute",
    "CanPlaceCounter": "game.card.face.attribute.can_place_counter",
    "CanPlaceToken": "game.card.face.attribute.can_place_token",
    "CanAttacked": "game.card.face.attribute.can_attacked",
    "HasAccelerationIcon": "game.card.face.attribute.has_acceleration_icon",
    "CanAccelerationToken": "game.card.face.attribute.can_acceleration_token",
    "CanAttach": "game.card.face.attribute.can_attach",
    "HasAmplify": "game.card.face.attribute.has_amplify",
    "HasAttack": "game.card.face.attribute.can_attack",
    "CanAttack": "game.card.face.attribute.can_attack",
    "CanBoost": "game.card.face.attribute.can_boost",
    "CanCrisis": "game.card.face.attribute.has_crisis",
    "HasDefense": "game.card.face.attribute.can_defense",
    "CanDefense": "game.card.face.attribute.can_defense",
    "HasHazard": "game.card.face.attribute.has_hazard",
    "CanHealth": "game.card.face.attribute.can_health",
    "CanHinder": "game.card.face.attribute.can_hinder",
    "CanIncite": "game.card.face.attribute.can_incite",
    "HasRecover": "game.card.face.attribute.can_recover",
    "CanRecover": "game.card.face.attribute.can_recover",
    "CanRetaliate": "game.card.face.attribute.can_retaliate",
    "HasScheme": "game.card.face.attribute.can_scheme",
    "CanScheme": "game.card.face.attribute.can_scheme",
    "CanSurge": "game.card.face.attribute.can_surge",
    "HasThwart": "game.card.face.attribute.can_thwart",
    "CanThwart": "game.card.face.attribute.can_thwart",
    "HasVictory": "game.card.face.attribute.has_victory",
    "HasSetup": "game.card.face.attribute.has_setup",
    "HasStarting": "game.card.face.attribute.has_starting",
    "HasUses": "game.card.face.attribute.has_uses",
    "HasHandSize": "game.card.face.attribute.has_hand_size",
    "HasModify": "game.card.face.attribute.has_modify",
    "HasStage": "game.card.face.attribute.has_stage",
    "HasBoostIcon": "game.card.face.attribute.has_boost_icon",
    "HasCost": "game.card.face.attribute.has_cost",
    "HasAssault": "game.card.face.attribute.has_assault",
    "HasForm": "game.card.face.attribute.has_form",
    "HasRestricted": "game.card.face.attribute.has_restricted",
    "HasResourceIcon": "game.card.face.attribute.has_resources",
    "HasPermanent": "game.card.face.attribute.has_permanent",
    "HasTemporary": "game.card.face.attribute.has_temporary",
    "HasTeamUp": "game.card.face.attribute.has_teamup",
    "CanTeamwork": "game.card.face.attribute.can_teamwork",
    "HasAlliance": "game.card.face.attribute.has_alliance",
    "CanQuickstrike": "game.card.face.attribute.can_quickstrike",
    "HasGuard": "game.card.face.attribute.has_guard",
    "HasPatrol": "game.card.face.attribute.has_patrol",
    "HasVillainous": "game.card.face.attribute.has_villainous",
    "HasMaxPer": "game.card.face.attribute.has_max_per",
    "HasVulnerable": "game.card.face.attribute.has_vulnerable",
    "HasToughness": "game.card.face.attribute.has_toughness",
    "HasSteady": "game.card.face.attribute.has_steady",
    "HasStalwart": "game.card.face.attribute.has_stalwart",
    "CanStatus": "game.card.face.attribute.can_status",
    "CanNoStatus": "game.card.face.attribute.can_status",
    "HasPeril": "game.card.face.attribute.has_peril",
    "AbilityFactory": "game.ability.factory.ability_factory",
}
for _export_name, _module_name in _REAL_CLASS_EXPORTS.items():
    try:
        _module = __import__(_module_name, fromlist=[_export_name])
        globals()[_export_name] = getattr(_module, _export_name)
    except Exception:
        pass

