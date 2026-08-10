from . import *

# Army of One

def GetAbilities() -> Sequence['Ability']:

    def army_of_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        Faces.ReadyAll([hero], effect)


    return [
        AbilityFactory.ReduceCostToPlayThis(
            -1,
            each_card_you_control=CardFinder(card_type=Ally),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            army_of_one,
        ).SetPlay().SetLabel()
        .SetTarget("YourHero", canbe_ready=True),
    ]
