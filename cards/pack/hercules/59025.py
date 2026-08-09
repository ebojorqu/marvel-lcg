from . import *

# * Gilgamesh

def GetAbilities() -> Sequence['Ability']:

    def additional_cost(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> None:
        if not effect.GetInitiator().GetIdentity().HasTrait("ETERNAL"):
            Faces.GiveStatus([effect.GetInitiator().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.WhenPlayerWouldPlayCard(
            AbilityType.Interrupt,
            "You",
            "This",
            additional_cost,
        ).CanWorkOnlyInHand(),
    ]
