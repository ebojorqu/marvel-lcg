from . import *

# Roving Mobs

def GetAbilities() -> Sequence['Ability']:

    def roving_mobs_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        RevealAllVersusAll(effect, effect.GetInitiator())

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            roving_mobs_defeated,
        ),
    ]
