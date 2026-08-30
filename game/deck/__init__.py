from core import Unused

__all__ = ["Deck", "Deck2", "DeckType", "SetAsideDeck"]


def __getattr__(name):
    if name in {"Deck", "Deck2", "DeckType"}:
        from game.deck.deck import Deck, Deck2, DeckType
        if name == "Deck":
            return Deck
        if name == "Deck2":
            return Deck2
        return DeckType
    if name == "SetAsideDeck":
        from game.deck.deck_aside import SetAsideDeck
        return SetAsideDeck
    raise AttributeError(name)


Unused(__all__)

