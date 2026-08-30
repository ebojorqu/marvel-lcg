from __future__ import annotations

from typing import TYPE_CHECKING, final

from engine.device.base.device import Device
from engine.log import Log

if TYPE_CHECKING:
    from engine.device.manager.base import DeviceManager

class OutputDevice(Device):

    @final
    def WaitSync(self) -> None:
        game = self.controller.game
        if not game.state.is_running:
            Log.DebugSilent("SYNC", f"WaitSync skip (Game is not running)")
            return
        return self.manager.DoWaitSync(self.player_id, self.IsSyncReady)

    def IsSyncReady(self) -> bool:
        ...

    def Render(self) -> None:
        ...

