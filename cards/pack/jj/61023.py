from . import *
from game.card.face.attribute.can_thwart import ThwartProperty

# Grapnel Launcher

def GetAbilities() -> Sequence['Ability']:

    def grapnel_launcher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        hero = effect.GetInitiator().GetHero()
        hero.BasicThwart(
            effect.targets,
            effect,
            property=ThwartProperty(additional_value=1, is_basic_power=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            grapnel_launcher,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Scheme2)
        .SetIgnoreKeyword('Patrol', 'Crisis'),
    ]