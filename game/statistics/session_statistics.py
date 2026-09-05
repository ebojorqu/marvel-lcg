from typing import TypeAlias
from core import *
# from engine.lib import Json
from game.card.face import *

KEY_NAME: TypeAlias = Literal['damage_dealt', 'damage_taken', 'thwarted_threat', 'entered_play']
META_KEY_NAME: TypeAlias = Literal['owner_id', 'card_id', 'name', 'set_name']

class SessionCardStatistics(TypedDict, total=False):
    damage_dealt: int
    damage_taken: int
    thwarted_threat: int
    entered_play: int
    owner_id: int
    card_id: str
    name: str
    set_name: str

class SessionStatistics:

    def __init__(self) -> None:
        self.dic: Dict[int, SessionCardStatistics] = {}
        self.DEFAULT_STATS = dict.fromkeys(get_args(KEY_NAME), 0)

    def Add(self, face: 'CardFace', value: int, name: KEY_NAME):
        if not PlayerCard.IsType(face):
            return
        id = face.card.object_id
        stats = self.dic.setdefault(id, self.DEFAULT_STATS.copy())
        owner_id = -1
        try:
            owner_id = face.GetOwnerPlayer().player_id
        except:
            owner_id = -1

        # Persist card metadata for robust frontend grouping/sorting when cards are no longer rendered.
        stats['owner_id'] = owner_id
        stats['card_id'] = face.paper.card_id
        stats['name'] = face.name
        stats['set_name'] = face.paper.set_name
        stats[name] += value

    # def Get(self) -> str:
    #     return Json.Dumps(self.dic)

