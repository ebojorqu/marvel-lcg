from . import *

# Terrestrial Invasion

def GetAbilities() -> Sequence['Ability']:

    def terrestrial_invasion(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["16063"]),
            card_type=Environment
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            terrestrial_invasion
        ),
    ]

