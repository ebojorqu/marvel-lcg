from . import *

# Herc's Helm

def GetAbilities() -> Sequence['Ability']:

    def hercs_helm(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            hercs_helm,
            conditions=[
                lambda effect, message: message.would_atk_message is not None,
                lambda effect, message: message.trigger.IsName("Hercules"),
                lambda effect, message: message.would_atk_message.attacker.IsVillain(),
            ],
        ).SetLabel("defense").SetCostFunc(CostFunc.Exhaust("This")),
    ]
