from __future__ import annotations

from typing import TYPE_CHECKING

from core import *
from engine.device.base.device import Device
from engine.device.manager.base import AskOptionPayload

if TYPE_CHECKING:
    from engine.device.manager.base import DeviceManager

class InputDevice(Device):

    @final
    def GetInput(self, data: AskOptionPayload) -> str|None:
        return self.manager.DoGetInput(data, self.player_id, self.IsInputReady)

    def IsInputReady(self) -> bool:
        ...

    @final
    def WaitConnect(self) -> None:
        self.manager.DoWaitConnect(self.player_id, self.IsConnect)
        self.is_connected = True

    def IsConnect(self) -> bool:
        ...

