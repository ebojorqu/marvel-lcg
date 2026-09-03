from . import *

# The Missing Milano

def GetAbilities() -> Sequence['Ability']:

    def the_missing_milano(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["16085a", "16085b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_name=LIBRARY_LABYRINTH,
        )

        villain = Worlds.FindVillain(effect)

        faces = SetupCards.SetAsideCards(
            effect,
            set_name="Ship Command",
        )
        assert villain
        GetShipCommand(effect).Create(effect, villain, type=DeckType.AsideDeck, has_discard_pile=False)
        GetShipCommand(effect).PushCards(faces, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            the_missing_milano
        ),
    ]

