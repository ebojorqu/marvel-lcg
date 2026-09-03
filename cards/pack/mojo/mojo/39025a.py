from . import *

# MojoMania

def GetAbilities() -> Sequence['Ability']:

    def mojomania(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["39026a", "39026b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_trait="SPINNING",
        )


    return [
        AbilityFactory.SetModularSetsAside(lambda effect: 1 + 1 * Worlds.GetPlayerNumIcon(effect)),
        AbilityFactory.WhenCardSetup(
            "This",
            mojomania
        ),
    ]

