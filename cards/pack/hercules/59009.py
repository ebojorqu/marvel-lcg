from . import *

# The Gift of Battle

def GetAbilities() -> Sequence['Ability']:

    def gift_of_battle(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(effect.targets, 5, effect)

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
            gift_of_battle,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
