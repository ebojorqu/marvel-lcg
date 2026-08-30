from core import *
from core import *
from game.card.face.base.unit import Unit2
from game.card.face.card_face import CardFace
from game.message.sender.sender import Message
from game.ability.ability import Ability
from cards.paper import Paper

class Friend(Unit2):
    @override
    def __init__(self, paper: 'Paper') -> None:
        super().__init__(paper)

    def GetBasicPowerEffects(self, powers: List["CardFace.BASIC_POWER"]) -> List['Effect']:
        powers_set = set(powers)
        return [x for x in self.effects if x.ability.func_names & powers_set]

