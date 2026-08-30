from typing import Callable, List
import sys

from core import Unused

__all__ = [
    "Message", "Message2", "OnEvent",
    "ConditionType", "ConditionsType", "OperationType",
    "CanBeInstead", "AttackerMessageInternal", "AttackerNoneOldMessage",
    "AttackerNoneMessage", "AttackerMessage", "SchemerMessage", "ThwarterMessage",
    "DefenderNoneMessage", "DefenderMessage", "TriggerFaceMessage", "TriggerMessage",
    "TriggerNonePlayerMessage", "TriggerPlayerMessage", "TriggerSchemeMessage",
    "TriggerUnitMessage", "TargetsMessage", "CanGainValueMessage",
]


def __getattr__(name):
    if name == "Message2":
        module = sys.modules.get("game.message.message")
        if module is not None:
            return getattr(module, "Message2")
        from game.message.message import Message2
        return Message2
    if name == "Message":
        module = sys.modules.get("game.message.sender.sender")
        if module is not None:
            return getattr(module, "Message")
        from game.message.sender.sender import Message
        return Message
    if name == "OnEvent":
        module = sys.modules.get("game.message.on_event.on_event")
        if module is not None:
            return getattr(module, "OnEvent")
        from game.message.on_event import OnEvent
        return OnEvent
    if name == "ConditionType":
        return Callable[["Effect", "Message2"], bool]
    if name == "ConditionsType":
        return List[Callable[["Effect", "Message2"], bool]]
    if name == "OperationType":
        return Callable[["Effect", "Message2"], None]
    if name in {
        "CanBeInstead", "AttackerMessageInternal", "AttackerNoneOldMessage",
        "AttackerNoneMessage", "AttackerMessage", "SchemerMessage", "ThwarterMessage",
        "DefenderNoneMessage", "DefenderMessage", "TriggerFaceMessage", "TriggerMessage",
        "TriggerNonePlayerMessage", "TriggerPlayerMessage", "TriggerSchemeMessage",
        "TriggerUnitMessage", "TargetsMessage", "CanGainValueMessage",
    }:
        import game.message.message_type as mt
        return getattr(mt, name)
    raise AttributeError(name)

Unused(__all__)

