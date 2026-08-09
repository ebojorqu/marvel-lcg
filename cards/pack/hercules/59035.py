from . import *

# Appeal to Athena

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            RemoveThisFromGame,
            conditions=[
                lambda effect, message: effect.GetInitiator().form.IsInAlterEgoForm(),
            ],
        ).SetCost(Cost("YY")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            RemoveThisFromGame,
            conditions=[
                lambda effect, message: effect.GetInitiator().form.IsInAlterEgoForm(),
            ],
        ).SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
