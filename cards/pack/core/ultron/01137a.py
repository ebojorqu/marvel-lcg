from . import *

# The Crimson Cowl - 1A

def GetAbilities() -> Sequence['Ability']:

    def the_crimson_cowl(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["01140"]),
            card_type=Environment,
            from_where=["SetAside"],
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            the_crimson_cowl
        ),
    ]
