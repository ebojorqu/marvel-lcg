from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.ability import AbilityType
    from game.effect.effect import Effect
    from game.message.message import Message2
    from game.message.message_type import TriggerMessage

class Condition2:

    @staticmethod
    def ThisIsTrigger(effect: 'Effect', message: 'TriggerMessage'):
        from game.ability.condition import Condition
        return Condition.CheckWhichCard("This", message.trigger, effect)

