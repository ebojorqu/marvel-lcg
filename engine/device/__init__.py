import sys

from core import Unused

__all__ = ["Device", "OutputDevice", "InputDevice", "DeviceManager"]


class _BootPlaceholder:
    pass


def __getattr__(name):
    if name == "Device":
        module = sys.modules.get("engine.device.base.device")
        if module is not None:
            return getattr(module, "Device", _BootPlaceholder)
        from engine.device.base.device import Device
        return Device
    if name == "OutputDevice":
        module = sys.modules.get("engine.device.base.output")
        if module is not None:
            return getattr(module, "OutputDevice", _BootPlaceholder)
        from engine.device.base.output import OutputDevice
        return OutputDevice
    if name == "InputDevice":
        module = sys.modules.get("engine.device.base.input")
        if module is not None:
            return getattr(module, "InputDevice", _BootPlaceholder)
        from engine.device.base.input import InputDevice
        return InputDevice
    if name == "DeviceManager":
        module = sys.modules.get("engine.device.manager.base")
        if module is not None:
            return getattr(module, "DeviceManager", _BootPlaceholder)
        from engine.device.manager.base import DeviceManager
        return DeviceManager
    raise AttributeError(name)

Unused(__all__)

