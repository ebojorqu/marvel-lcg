import sys

from core import Unused

__all__ = ["OnEvent"]


def __getattr__(name):
    if name == "OnEvent":
        module = sys.modules.get("game.message.on_event.on_event")
        if module is not None:
            return getattr(module, "OnEvent")
        from game.message.on_event.on_event import OnEvent
        return OnEvent
    raise AttributeError(name)


Unused(__all__)

