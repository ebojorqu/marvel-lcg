from . import *

# "We Are Groot"

def GetAbilities() -> Sequence['Ability']:

    def we_are_groot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        counter = effect.cost_func.Get(CostFunc.Counter).return_remove_counter
        targets = effect.GetInitiator().AskChooseFaces(
            effect.targets,
            (counter, counter),
            effect,
            prompt="Choose characters to receive Tough",
        )
        Faces.GiveStatus(targets, "Tough", effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            we_are_groot
        ).SetPlay().SetLabel()
        .SetTarget(Friend, range=(1, "All"))
        .SetCostFunc(CostFunc.Counter(CardFinder(name="Groot"), (1, 4), 'growth')),
    ]

