from . import *

# Olympus

def GetAbilities() -> Sequence['Ability']:

    def olympus_resources(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        gifts = GetGiftCount(message.GetToPlayer())
        return Resources("G") * gifts

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=olympus_resources,
            conditions=[
                lambda effect, message: GetGiftCount(message.GetToPlayer()) > 0,
            ],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
