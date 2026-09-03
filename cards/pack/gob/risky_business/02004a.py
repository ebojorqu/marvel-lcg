from . import *

# Hostile Takeover - 1A

def GetAbilities() -> Sequence['Ability']:

    def hostile_takeover(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["02006a", "02006b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_name="Criminal Enterprise",
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            hostile_takeover
        )
    ]
