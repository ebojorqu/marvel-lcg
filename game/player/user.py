from core import *
from game.object.object import Object
from game.world.game_area import *
from game.card.face import *

if TYPE_CHECKING:
    from game.world.world import World

class User(Object):
    def __init__(self, name: Literal['player', 'scenario'], world: 'World'):
        self.is_scenario: bool
        self.is_eliminated = False
        super().__init__(name, world)

    def __repr__(self) -> str:
        from game.player import Player
        from game.player import Scenario
        assert isinstance(self, Player|Scenario), f"{self=} {type(self)=}"
        return self.name
        # return f'[{self.name}]'

    @final
    def IsScenario(self) -> bool:
        return self.is_scenario

    def IsPlayer(self) -> bool:
        return False

    def GetRoleCharacter(self) -> 'Identity|Villain':
        assert False

    ################################################################################
    #
    def GetGameArea(self) -> 'GameArea':
        assert False, f"You need to override this function, {self=}"

