from core import Unused

__all__ = ["Select", "Selector", "SELECT"]


class _LazySelectorExport:
    def __init__(self, target_name: str):
        self._target_name = target_name

    def _resolve(self):
        if self._target_name == "Select":
            from game.selector.factory import Select
            return Select
        if self._target_name == "Selector":
            from game.selector.selector import Selector
            return Selector
        if self._target_name == "SELECT":
            from game.selector.factory import SELECT
            return SELECT
        raise AttributeError(self._target_name)

    def __call__(self, *args, **kwargs):
        return self._resolve()(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._resolve(), name)

    def __repr__(self):
        return f"<lazy selector export {self._target_name}>"


Select = _LazySelectorExport("Select")
Selector = _LazySelectorExport("Selector")
SELECT = _LazySelectorExport("SELECT")

Unused(__all__)

