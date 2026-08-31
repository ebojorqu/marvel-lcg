from core import *
from game.card.face import *
from game.card.face.base.final_type import FinalType as _FinalType
from game.ability import *
from game.message import *
from game.player import *
from game.deck import *

@final
class EncounterVillain(Villain, _FinalType):
    pass

