from . import *

# Gauntlets of Hercules

def GetAbilities() -> Sequence['Ability']:

    def gauntlets_of_hercules(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        gifts = GetGiftCount(effect.GetInitiator())
        if gifts > 0:
            message.defender.TemporaryGain(effect, message.would_atk_message, retaliate=gifts)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "You",
            gauntlets_of_hercules,
            against_who=Enemy,
            conditions=[
                lambda effect, message: message.defender.IsName("Hercules"),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
