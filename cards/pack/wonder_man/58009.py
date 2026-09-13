from . import *

# Mr. Hollywood

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
            only_for_overpay=True,
        ).LimitOncePerEvent(),
    ]