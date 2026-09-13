from . import *

# * Swordsman: Jacques Duquesne

def GetAbilities() -> Sequence['Ability']:

    def swordsman_response(effect: 'Effect', message: 'Message.AfterCardBecomeBoost') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        boost_message = message.boost_message
        boost_message.being_message.DeclareDefender(this, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            is_basic_attack=True,
            piercing=True,
        ),
        AbilityFactory.AfterCardBecomeBoost(
            AbilityType.HeroResponse,
            None,
            swordsman_response,
            conditions=[
                lambda effect, message:
                    isinstance(message.boost_message.being_message, Message.WhenUnitBeingAttack),
                lambda effect, message:
                    message.boost_message.being_message.would_atk_message.GetDefender() is None,
                lambda effect, message:
                    effect.this.GetControlByPlayer() == message.boost_message.GetToPlayer(),
            ]
        ),
    ]