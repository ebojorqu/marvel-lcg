import sys

from core import Unused

__all__ = ["Condition", "Condition2"]


def __getattr__(name):
    if name == "Condition":
        module = sys.modules.get("game.ability.condition.condition")
        if module is not None:
            return getattr(module, "Condition")
        from game.ability.condition.condition import Condition
        return Condition
    if name == "Condition2":
        module = sys.modules.get("game.ability.condition.condition2")
        if module is not None:
            return getattr(module, "Condition2")
        from game.ability.condition.condition2 import Condition2
        return Condition2
    raise AttributeError(name)


Unused(__all__)

