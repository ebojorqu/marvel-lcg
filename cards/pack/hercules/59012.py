from . import *

# Olympus

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=lambda effect, message: Resources("W") * GetGiftCount(effect.GetInitiator()),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
