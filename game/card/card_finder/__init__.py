import sys

from core import Unused

__all__ = ["CardFinder", "CardFinder2", "CardFinderHelper"]


def __getattr__(name):
    if name in {"CardFinder", "CardFinder2"}:
        module = sys.modules.get("game.card.card_finder.finder")
        if module is not None:
            return getattr(module, "CardFinder" if name == "CardFinder" else "CardFinder2")
        from game.card.card_finder.finder import CardFinder, CardFinder2
        return CardFinder if name == "CardFinder" else CardFinder2
    if name == "CardFinderHelper":
        module = sys.modules.get("game.card.card_finder.helper")
        if module is not None:
            return getattr(module, "CardFinderHelper")
        from game.card.card_finder.helper import CardFinderHelper
        return CardFinderHelper
    raise AttributeError(name)


Unused(__all__)

