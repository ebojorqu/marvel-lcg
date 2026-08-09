from . import *

# Prince of Power

def GetAbilities() -> Sequence['Ability']:

    def prince_of_power(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        total_excess = sum(x.excess_damage for x in message.atk_messages if x.has_defeated_target)
        if total_excess > 0:
            effect.GetInitiator().GetHero().Heal(total_excess, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.HeroResponse,
            "You",
            prince_of_power,
            is_basic_attack=True,
            conditions=[
                lambda effect, message: message.attacker.IsName("Hercules"),
                lambda effect, message: any(x.has_defeated_target for x in message.atk_messages),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
