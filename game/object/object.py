from typing import Final, TYPE_CHECKING
from core import *

if TYPE_CHECKING:
    from game.object.manager import ObjectManager
    from game.world.world import World

class Object:

    def __init__(self, category: 'ObjectManager.OBJECT_CATEGORY', world: 'World') -> None:
        object_id = world.object_manager.AddObject(category, self)

        self.object_id      : Final = object_id
        self.object_category: Final = category

        self.world = world

