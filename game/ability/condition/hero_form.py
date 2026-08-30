from typing import TYPE_CHECKING
from core import *

if TYPE_CHECKING:
    from game.effect.effect import Effect
    from game.player import Player
    from game.card.face.card_face import CardFace

class ConditionHeroForm:

    @staticmethod
    def PlayerInMassForm(card_type: 'CardFinder|Player|Literal["You"]', form: 'Form.FORM_TYPE', effect: 'Effect') -> bool:
        from game.operate.worlds import Worlds
        from game.player import Player

        if card_type == "You":
            initiator = effect.GetInitiator()
        elif isinstance(card_type, Player):
            initiator = card_type
        else:
            face = Worlds.FindCardOnField(
                effect,
                card_type,
                check_face_fn=lambda face:
                    Player.IsType(face.GetControlBy())
            )
            if face:
                initiator = face.GetControlByPlayer()
            else:
                return False
        return initiator.form.IsFormInternal(form)

    @staticmethod
    def YouAreInHeroFrom(effect: 'Effect', trait: "CardFace.TRAITS") -> bool:
        initiator = effect.GetInitiator()
        return initiator.IsInHeroForm(trait)

