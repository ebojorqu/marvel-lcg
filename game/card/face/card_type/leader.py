# from typing import Callable, Dict, List, Sequence, final
from core import *
from game.card.face import *
from game.card.face.base.final_type import FinalType as _FinalType
from game.ability import *
from game.message import *
from game.player import *
from game.deck import *
# from cards.paper import Paper
# from game.element.damage_property import DamageProperty

@final
class Leader(Villain, _FinalType):
    pass
