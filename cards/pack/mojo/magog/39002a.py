from . import *

# Melee in the Mojo-seum

def GetAbilities() -> Sequence['Ability']:

    def melee_in_the_mojo_seum_revealed(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["39003a", "39003b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_trait="BOOING CROWD",
        )
        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["39004a", "39004b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_trait="BOOING CROWD",
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            melee_in_the_mojo_seum_revealed
        ),
    ]

