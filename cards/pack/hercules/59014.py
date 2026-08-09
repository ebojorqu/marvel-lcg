from . import *

# Golden Mace

def GetAbilities() -> Sequence['Ability']:

    def golden_mace(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        gifts = GetGiftCount(effect.GetInitiator())
        message.GainATKForThisAttack(gifts, effect)
        message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            golden_mace,
            is_basic_attack=True,
            conditions=[
                lambda effect, message: message.attacker.IsName("Hercules"),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
