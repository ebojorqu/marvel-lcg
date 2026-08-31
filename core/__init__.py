def Unused(*_: object):
    pass

import builtins
import importlib
import sys

try:
    from typing_extensions import override, final
except ImportError:  # pragma: no cover - compatibility fallback for older runtimes
    def override(func=None, /, **kwargs):
        if func is None:
            def decorator(target):
                return target
            return decorator
        return func

    def final(func=None, /, **kwargs):
        if func is None:
            def decorator(target):
                return target
            return decorator
        return func

builtins.override = override
builtins.final = final

from typing import Any, Callable, Dict, List, Sequence, Type, Set, Tuple, Literal, Optional
Unused(Any)
Unused(Dict, List, Set, Tuple, Sequence)
Unused(Type[Callable[[], Any]])
Unused(Literal, Optional)

for _name, _value in {
    "Any": Any,
    "Callable": Callable,
    "Dict": Dict,
    "List": List,
    "Sequence": Sequence,
    "Type": Type,
    "Set": Set,
    "Tuple": Tuple,
    "Literal": Literal,
    "Optional": Optional,
}.items():
    setattr(builtins, _name, _value)

# from typing import TypeAlias
# Unused(TypeAlias)

# from typing import Final
# Unused(Final)
# from typing_extensions import Final
# Unused(Final)

from typing import TYPE_CHECKING, TypeVar
from core.meta_class.class_name import ClassNameMeta
Unused(TYPE_CHECKING)
Unused(TypeVar)

TC = TypeVar("TC")
TF = TypeVar("TF")
TP = TypeVar("TP")
T = TypeVar("T")
TM = TypeVar("TM")
TMP = TypeVar("TMP")
INT_TYPE = int | str

TYPE_CHECKING = False

# These project modules use many annotation references like Message, User, Player,
# CardFace, etc. during import-time class creation. Keep the placeholders simple but
# compatible with nested attribute access while the real modules finish bootstrapping.
class _PlaceholderMetaBase(ClassNameMeta):
    def _resolve_runtime(self, cls):
        return _resolve_runtime_placeholder(cls.__name__)

    def __getattr__(cls, name):
        resolved = cls._resolve_runtime(cls)
        if resolved is not None and resolved is not cls:
            return getattr(resolved, name)
        return type(name, (), {})

    def __mro_entries__(cls, bases):
        resolved = cls._resolve_runtime(cls)
        if resolved is not None and resolved is not cls:
            return (resolved,)
        return bases

    def __getitem__(cls, item):
        return item

    def __instancecheck__(cls, instance):
        resolved = cls._resolve_runtime(cls)
        if resolved is not None and resolved is not cls:
            return isinstance(instance, resolved)
        return super().__instancecheck__(instance)

    def __subclasscheck__(cls, subclass):
        resolved = cls._resolve_runtime(cls)
        if resolved is not None and resolved is not cls:
            return issubclass(subclass, resolved)
        return super().__subclasscheck__(subclass)

    def __call__(cls, *args, **kwargs):
        resolved = cls._resolve_runtime(cls)
        if resolved is not None and resolved is not cls:
            return resolved(*args, **kwargs)
        return super().__call__(*args, **kwargs)

class _PlaceholderMeta(_PlaceholderMetaBase):
    pass

class _GenericPlaceholderMeta(_PlaceholderMetaBase):
    pass


def _resolve_runtime_placeholder(name: str):
    known = {
        "Message": "game.message.sender.sender",
        "User": "game.player.user",
        "Player": "game.player.player",
        "Effect": "game.effect.effect",
        "World": "game.world.world",
        "Scenario": "game.player.scenario",
        "CardFace": "game.card.face.card_face",
        "Deck": "game.deck.deck",
        "GameArea": "game.world.game_area.game_area",
        "Ability": "game.ability.ability",
        "Condition": "game.ability.condition.condition",
        "OnEvent": "game.event.on_event",
        "Unit2": "game.card.face.base.unit",
        "Scheme2": "game.card.face.base.scheme",
        "Selector": "game.selector.selector",
        "Villain": "game.card.face.base.villain",
        "Enemy": "game.card.face.base.enemy",
        "Friend": "game.card.face.base.friend",
        "EncounterCard": "game.card.face.base.card_encounter",
        "EncounterNonVillainCard": "game.card.face.base.card_encounter",
        "PlayerCard": "game.card.face.base.card_player",
        "ClassCard": "game.card.face.base.card_player",
        "MainScheme": "game.card.face.card_type.scheme_main",
        "PlayerSideScheme": "game.card.face.card_type.scheme_player",
        "EncounterSideScheme": "game.card.face.card_type.scheme_side",
        "Hero": "game.card.face.card_type.identity",
        "AlterEgo": "game.card.face.card_type.identity",
        "Identity": "game.card.face.card_type.identity",
        "Ally": "game.card.face.card_type.ally",
        "Asset2": "game.card.face.base.asset",
        "Buff": "game.buff.buff",
        "Scheme": "game.card.face.base.scheme",
        "SchemeSide2": "game.card.face.base.scheme_side",
        "FinalType": "game.card.face.base.final_type",
        "StatusCard": "game.card.face.card_type.card_status",
        "Insert": "game.card.face.card_type.insert",
        "Challenge": "game.card.face.card_type.insert",
        "Minion": "game.card.face.card_type.minion",
        "Leader": "game.card.face.card_type.leader",
        "Environment": "game.card.face.card_type.environment",
        "Upgrade": "game.card.face.card_type.upgrade",
        "Support": "game.card.face.card_type.support",
        "Attachment": "game.card.face.card_type.attachment",
        "Event": "game.card.face.card_type.event",
        "Obligation": "game.card.face.card_type.obligation",
        "Treachery": "game.card.face.card_type.treachery",
        "Resource": "game.card.face.card_type.resource",
        "Evidence": "game.card.face.card_type.evidence",
        "AbilityType": "game.ability.ability_type",
        "TimingPriority": "game.ability.ability_type",
    }

    module_name = known.get(name)
    if module_name is not None:
        module = sys.modules.get(module_name)
        if module is None:
            try:
                module = importlib.import_module(module_name)
            except Exception:
                module = None
        if module is not None:
            value = getattr(module, name, None)
            if value is not None and value.__name__ == name:
                return value

    for module in list(sys.modules.values()):
        if module is None:
            continue
        value = getattr(module, name, None)
        if value is not None and getattr(value, "__name__", None) == name:
            module_name_attr = getattr(value, "__module__", "")
            if module_name_attr != __name__:
                return value

    return None


def _make_placeholder(name: str, *, generic: bool = False):
    meta = _GenericPlaceholderMeta if generic else _PlaceholderMeta
    return meta(name, (), {"__module__": __name__})


Message = _make_placeholder("Message")
User = _make_placeholder("User")
Player = _make_placeholder("Player")
Effect = _make_placeholder("Effect")
World = _make_placeholder("World")
Scenario = _make_placeholder("Scenario")
CardFace = _make_placeholder("CardFace")
Deck = _make_placeholder("Deck")
GameArea = _make_placeholder("GameArea")
Ability = _make_placeholder("Ability")
Condition = _make_placeholder("Condition")
OnEvent = _make_placeholder("OnEvent")
Unit2 = _make_placeholder("Unit2")
Scheme2 = _make_placeholder("Scheme2")
Selector = _make_placeholder("Selector")
Villain = _make_placeholder("Villain")
Enemy = _make_placeholder("Enemy")
Friend = _make_placeholder("Friend")
EncounterCard = _make_placeholder("EncounterCard")
EncounterNonVillainCard = _make_placeholder("EncounterNonVillainCard")
PlayerCard = _make_placeholder("PlayerCard")
ClassCard = _make_placeholder("ClassCard")
MainScheme = _make_placeholder("MainScheme")
PlayerSideScheme = _make_placeholder("PlayerSideScheme")
EncounterSideScheme = _make_placeholder("EncounterSideScheme")
Hero = _make_placeholder("Hero")
AlterEgo = _make_placeholder("AlterEgo")
Identity = _make_placeholder("Identity")
Ally = _make_placeholder("Ally")
Asset2 = _make_placeholder("Asset2")
Buff = _make_placeholder("Buff")
Scheme = _make_placeholder("Scheme")
SchemeSide2 = _make_placeholder("SchemeSide2")
FinalType = _make_placeholder("FinalType")
StatusCard = _make_placeholder("StatusCard")
Insert = _make_placeholder("Insert")
Challenge = _make_placeholder("Challenge")
Minion = _make_placeholder("Minion")
Leader = _make_placeholder("Leader")
Environment = _make_placeholder("Environment")
Upgrade = _make_placeholder("Upgrade")
Support = _make_placeholder("Support")
Attachment = _make_placeholder("Attachment")
Event = _make_placeholder("Event")
Obligation = _make_placeholder("Obligation")
Treachery = _make_placeholder("Treachery")
Resource = _make_placeholder("Resource")
Evidence = _make_placeholder("Evidence")
Deck2 = _make_placeholder("Deck2", generic=True)
CardFinder = _make_placeholder("CardFinder", generic=True)
CardFinder2 = _make_placeholder("CardFinder2", generic=True)
AbilityType = _make_placeholder("AbilityType")
TimingPriority = _make_placeholder("TimingPriority")

class _GenericTypeAlias:
    def __class_getitem__(cls, item):
        return object
    __getitem__ = __class_getitem__

ConditionType = _GenericTypeAlias
ConditionsType = _GenericTypeAlias
OperationType = _GenericTypeAlias
AbilitiesType = _GenericTypeAlias
CardType = _GenericTypeAlias
CardTypeMin = _GenericTypeAlias
EventType = _GenericTypeAlias
PlayerType = _GenericTypeAlias
DeckType = _make_placeholder("DeckType")

for _name, _value in {
    "Message": Message,
    "User": User,
    "Player": Player,
    "Effect": Effect,
    "World": World,
    "Scenario": Scenario,
    "CardFace": CardFace,
    "Deck": Deck,
    "GameArea": GameArea,
    "Ability": Ability,
    "Condition": Condition,
    "OnEvent": OnEvent,
    "Unit2": Unit2,
    "Scheme2": Scheme2,
    "Selector": Selector,
    "Villain": Villain,
    "Enemy": Enemy,
    "Friend": Friend,
    "EncounterCard": EncounterCard,
    "EncounterNonVillainCard": EncounterNonVillainCard,
    "PlayerCard": PlayerCard,
    "ClassCard": ClassCard,
    "MainScheme": MainScheme,
    "PlayerSideScheme": PlayerSideScheme,
    "EncounterSideScheme": EncounterSideScheme,
    "Hero": Hero,
    "AlterEgo": AlterEgo,
    "Identity": Identity,
    "Ally": Ally,
    "Asset2": Asset2,
    "Buff": Buff,
    "Scheme": Scheme,
    "SchemeSide2": SchemeSide2,
    "FinalType": FinalType,
    "StatusCard": StatusCard,
    "Insert": Insert,
    "Challenge": Challenge,
    "Minion": Minion,
    "Leader": Leader,
    "Environment": Environment,
    "Upgrade": Upgrade,
    "Support": Support,
    "Attachment": Attachment,
    "Event": Event,
    "Obligation": Obligation,
    "Treachery": Treachery,
    "Resource": Resource,
    "Evidence": Evidence,
    "Deck2": Deck2,
    "CardFinder": CardFinder,
    "CardFinder2": CardFinder2,
    "AbilityType": AbilityType,
    "TimingPriority": TimingPriority,
    "ConditionType": ConditionType,
    "ConditionsType": ConditionsType,
    "OperationType": OperationType,
    "AbilitiesType": AbilitiesType,
    "CardType": CardType,
    "CardTypeMin": CardTypeMin,
    "Literal": Literal,
    "Optional": Optional,
    "EventType": EventType,
    "PlayerType": PlayerType,
    "DeckType": DeckType,
    "TC": TC,
    "TF": TF,
    "TP": TP,
    "T": T,
    "TM": TM,
    "TMP": TMP,
}.items():
    setattr(builtins, _name, _value)

_CARD_FACE_EXPORTS = [
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

for _name in _CARD_FACE_EXPORTS:
    if not hasattr(builtins, _name):
        _value = _make_placeholder(_name)
        globals()[_name] = _value
        setattr(builtins, _name, _value)

from typing import Literal
Unused(Literal)

from typing import Union
Unused(Union)

try:
    from typing import TypeGuard
except ImportError:
    from typing_extensions import TypeGuard
Unused(TypeGuard)

# The compatibility decorators are intentionally defined before any circular imports so
# modules can safely decorate methods during bootstrap.
Unused(override)
Unused(final)

from copy import copy
Unused(copy)

from dataclasses import dataclass, field
from dataclasses import asdict
from dataclasses import fields, is_dataclass
builtins.dataclass = dataclass
builtins.field = field
builtins.asdict = asdict
builtins.fields = fields
builtins.is_dataclass = is_dataclass
Unused(dataclass, field)
Unused(asdict)
Unused(fields, is_dataclass)

from typing import Generic, Iterable
Unused(Generic, Iterable)

from typing import Awaitable
Unused(Awaitable)

from typing import ForwardRef, cast, get_args, get_origin
Unused(ForwardRef, cast, get_args, get_origin)

from typing import TypedDict
Unused(TypedDict)

from typing_extensions import Unpack
Unused(Unpack)

from typing import NoReturn
Unused(NoReturn)

from typing import overload
Unused(overload)
from typing_extensions import deprecated
Unused(deprecated)

# from typing_extensions import NotRequired
# Unused(NotRequired)

from core.utility.types import Types
Unused(Types)
# Rotate, UnionTypeExtract, LiteralToList, LiteralToDict, RemoveDuplicates, StrListToList, ListToStrList
# Unused(Rotate, UnionTypeExtract, LiteralToList, LiteralToDict, RemoveDuplicates, StrListToList, ListToStrList)

from core.utility.system import System
Unused(System)

from core.utility.cast import Cast
Unused(Cast)

from core.utility.utility import Unquote
Unused(Unquote)

from core.utility.debug import Debug
Unused(Debug)

from core.utility.func import GetFuncLines, GetFuncName, GetCallStack, IsAsyncFunction, IsNonAsyncFunction
Unused(GetFuncLines, GetFuncName, GetCallStack, IsAsyncFunction, IsNonAsyncFunction)

from core.meta_class import Tracker
from core.meta_class.class_name import ClassNameMeta
Unused(Tracker)
Unused(ClassNameMeta)

from core.lib.math import Math
Unused(Math)

import collections
Unused(collections)

# `from core import *` is used widely during startup, so the compatibility layer must
# export the full runtime surface rather than a hand-maintained subset. This prevents
# circular bootstrap imports from silently dropping names like `dataclass` or `TypeVar`.
__all__ = [name for name in globals() if not name.startswith("_")]

