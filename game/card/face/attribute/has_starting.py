from . import *

class HasStarting(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_starting = 0

        super().__init__(paper)

        self.RegisterAttribute("Starting", "printed_starting")

    def CanIncludeInDeck(self, player: 'Player') -> bool:
        if not self.printed_starting:
            return True

        current_starting = sum(
            1
            for face in player.player_deck.GetAll()
            if HasStarting.IsType(face) and face.printed_starting > 0
        )
        return current_starting == 0

    def ProcessStarting(self, by_effect: 'Effect'):
        player = self.GetControlByOrOwner()
        if not Player.IsType(player):
            return

        choice = player.AskChooseOneText(
            [True, False],
            ["Add to your hand before drawing your starting hand", "Do not add to your hand"],
        )
        if choice:
            self.card.MoveToArea(player.hand_cards, by_effect, ui_group=True)
