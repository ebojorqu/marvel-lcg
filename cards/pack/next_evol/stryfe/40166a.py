from . import *

# Uncontrollable Power

def GetAbilities() -> Sequence['Ability']:

    def uncontrollable_power(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        if not Worlds.FindCardOnField(
            effect,
            name="Hope Summers",
        ):
            player = Worlds.GetFirstPlayer(effect)
            SetupCards.PutIntoPlay(
                effect,
                finder=CardFinder(card_ids=["40130"]),
                for_player=player,
                under_control=True,
            )

        SetupCards.Reveal(
            effect,
            name="Stryfe's Grasp",
        )

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            uncontrollable_power
        ),
    ]

