from __future__ import annotations

from core import *
from game.card.face.card_face import CardFace
from game.card.face.attribute.has_boost_icon import HasBoostIcon
from game.card.face.attribute.can_incite import CanIncite
from game.card.face.attribute.has_victory import HasVictory
from game.card.face.attribute.has_peril import HasPeril
from game.card.face.attribute.can_surge import CanSurge
from game.card.face.attribute.can_acceleration_token import CanAccelerationToken

class EncounterCard(CanSurge, CanAccelerationToken, CardFace):
    pass

class EncounterNonVillainCard(HasBoostIcon, CanIncite, HasVictory, HasPeril, EncounterCard):

    def IsNemesis(self, player: 'Player') -> bool:
        if not self.paper.set_name.endswith(" Nemesis"):
            return False
        identity = player.GetIdentity()
        from game.card.face.card_type import Minion
        if Minion.IsType(self):
            if not self.nemesis:
                return False
        # We cannot use this, see "01167" and "27058"
        #     return player.IsName(self.nemesis)
        if identity.paper.set_name == "Spider-Man - Miles Morales":
            return self.paper.set_name[:-8] == "Spider-Man - Morales"
        return identity.paper.set_name == self.paper.set_name[:-8]


