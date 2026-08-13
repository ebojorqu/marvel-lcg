from . import *

# Olympic Feud

def GetAbilities() -> Sequence['Ability']:

    def olympic_feud_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        olympus_cards = len(Worlds.FindCardsOnField(effect, CardFinder(trait="OLYMPUS")))
        if olympus_cards > 0:
            this.PlaceThreatOnSchemes([this], olympus_cards, effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            olympic_feud_revealed,
        ),
    ]
