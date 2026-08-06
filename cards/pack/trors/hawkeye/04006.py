from . import *

# Explosive Arrow

def GetAbilities() -> Sequence['Ability']:

    def explosive(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        chosen_player = effect.targets[0].GetControlByPlayer()
        targets = Worlds.GetVillains(effect) + chosen_player.GetEngagedMinions()

        this.DealDamage(targets, 3, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            explosive,
        ).SetPlay()
        .SetTarget("Players")
        .SetCostFunc(CostFunc.Exhaust(
            card_type=Upgrade,
            name=HAWKEYE_BOW_NAME,
            from_where=["YouControlCards"])
        )
    ]
