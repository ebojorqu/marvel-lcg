from . import *

# Wisdom of Athena

def GetAbilities() -> Sequence['Ability']:

    def wisdom_of_athena(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            1,
            each_card_you_control=CardFinder(trait="GIFT"),
            conditions=[
                lambda effect, message: GetGiftCount(effect.GetInitiator()) > 0,
            ],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wisdom_of_athena,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
