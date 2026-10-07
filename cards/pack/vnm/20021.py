from . import *

# Side Holster

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players",
        ),
        AbilityFactory.ThisGainKeyword(
            control_additional_restricted=CardFinder2("WEAPON", Upgrade),
        ),
    ]

