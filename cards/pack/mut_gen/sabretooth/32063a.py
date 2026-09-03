from . import *

# Stalked by Sabretooth 1A

def GetAbilities() -> Sequence['Ability']:

    def stalked_by_sabretooth_1a(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        scheme = SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["32065a", "32065b"]),
            card_type=SchemeSide2,
            from_where=["SetAside"],
            flip_to_name="Find the Senator",
        )
        if scheme:
            SetupCards.AttachTo(
                effect,
                scheme,
                finder=ROBERT_KELLY_FINDER,
                card_type=Ally
            )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            stalked_by_sabretooth_1a
        ),
    ]

