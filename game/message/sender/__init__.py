from typing import TYPE_CHECKING

from core import *

if TYPE_CHECKING:
    from game.effect.effect import Effect
    from game.player import Player
    from game.world.world import World
    from game.world.game_area.game_area import GameArea

# Importing this during __init__ time pulls in engine/world/scene layers too early,
# which re-enters the circular bootstrap chain. Keep the runtime dependency deferred.

from game.message.message import Message2
from game.message.message_type import *
Unused(Message2)
Unused(CalculateMessage)
Unused(CanBeInstead)
Unused(CanGainValueMessage)
Unused(CardStateUpdatedMessage)
Unused(CheckIfMessage)
Unused(GettingMessage)
Unused(CheckNoneMessage)
Unused(DamageMessage)
Unused(DeckMessage)
Unused(DefenderMessage)
Unused(HasEndEventMessage)
Unused(HasPreEventMessage)
Unused(InActivationMessage)
Unused(LikeFakeMessage)
Unused(NoSendMessage)
Unused(NoSendResolve)
Unused(SchemerMessage)
Unused(TargetsMessage)
Unused(TextMessage)
Unused(ThwarterMessage)
Unused(TriggerFaceMessage)
Unused(TriggerNonePlayerMessage)
Unused(TriggerPlayerMessage)
Unused(TriggerSchemeMessage)
Unused(TriggerUnitMessage)

