import sys

from core import Unused

__all__ = ["DeviceManager"]


class _BootPlaceholder:
    pass


def __getattr__(name):
    if name == "DeviceManager":
        module = sys.modules.get("engine.device.manager.base")
        if module is not None:
            return getattr(module, "DeviceManager", _BootPlaceholder)
        from engine.device.manager.base import DeviceManager
        return DeviceManager
    raise AttributeError(name)


Unused(__all__)

