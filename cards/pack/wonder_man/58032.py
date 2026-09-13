from . import *

# Coordinated Effort

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(
                card_type=EncounterCard,
                is_face_up=True,
                not_with_attach=CardFinder(name="58032"),
            )
        ),
    ]
