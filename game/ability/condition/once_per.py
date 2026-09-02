from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.effect.effect import Effect
    from game.message.message import Message2
    from game.ability.ability import Ability

def GetForDelayAbility(effect: 'Effect') -> 'Ability|None':
    # if effect.ability.type.is_delay_ability:
    #     return effect.delay_ability
    return effect.ability

class ConditionOncePer:

    @staticmethod
    def LimitOncePerRound(effect: 'Effect', message: 'Message2') -> bool:
        world = effect.world
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerRound(ability)

    @staticmethod
    def LimitOncePerRoundPerPlayer(effect: 'Effect', message: 'Message2') -> bool:
        from game.message.sender.sender import TriggerNonePlayerMessage
        assert isinstance(message, TriggerNonePlayerMessage)
        world = effect.world
        player = message.GetToPlayer()
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerRoundPerPlayer(ability, player)

    @staticmethod
    def LimitOncePerPhasePerPlayer(effect: 'Effect', message: 'Message2') -> bool:
        from game.message.sender.sender import TriggerNonePlayerMessage
        assert isinstance(message, TriggerNonePlayerMessage)
        world = effect.world
        player = message.GetToPlayer()
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerPhasePerPlayer(ability, player)

    @staticmethod
    def LimitOncePerPhase(effect: 'Effect', message: 'Message2') -> bool:
        world = effect.world
        ability = GetForDelayAbility(effect)
        return world.stat.IsOncePerPhase(ability)

    @staticmethod
    def LimitOncePerEvent(effect: 'Effect', message: 'Message2') -> bool:
        ability = GetForDelayAbility(effect)
        return not any(x.ability == ability for x in message.once_per_event_effects)

    @staticmethod
    def LimitOnceCardNamePerEvent(effect: 'Effect', message: 'Message2') -> bool:
        ability = GetForDelayAbility(effect)
        if ability is None:
            return True
        return not any(x.ability.paper == ability.paper for x in message.once_per_event_effects)

