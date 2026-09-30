from . import *

# In Harm's Way

def GetAbilities() -> Sequence['Ability']:

    def in_harms_way(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        hero = effect.GetInitiator().GetHero()
        value = hero.defense

        this.DealDamage(effect.targets, value, effect)
        this.RemoveThreatFromSchemes(effect.targets2, value, effect)

    return [
        AbilityFactory.UpdateCostOfCardInternal(
            "This",
            lambda effect: len(effect.GetInitiator().GetControlCards(CardFinder(card_type=Ally))),
            "You",
            is_play=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            in_harms_way,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]