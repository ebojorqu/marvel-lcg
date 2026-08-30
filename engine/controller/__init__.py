import sys

from core import Unused

__all__ = ["Controller", "ControllerManager"]


class _BootPlaceholder:
    pass


def __getattr__(name):
    if name == "Controller":
        module = sys.modules.get("engine.controller.controller")
        if module is not None:
            return getattr(module, "Controller", _BootPlaceholder)
        from engine.controller.controller import Controller
        return Controller
    if name == "ControllerManager":
        module = sys.modules.get("engine.controller.manager")
        if module is not None:
            return getattr(module, "ControllerManager", _BootPlaceholder)
        from engine.controller.manager import ControllerManager
        return ControllerManager
    raise AttributeError(name)


Unused(__all__)

