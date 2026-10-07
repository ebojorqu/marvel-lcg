from . import *

# Rocket Launcher

def GetAbilities() -> Sequence['Ability']:

    def rocket_launcher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        chosen_player = effect.targets[0].GetControlByPlayer()
        targets = Worlds.GetVillains(effect) + chosen_player.GetEngagedMinions()

        this.DealDamage(targets, 2, effect)


    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'charge'),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rocket_launcher
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge'))
        .SetTarget("Players"),
    ]

