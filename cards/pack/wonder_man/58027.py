from . import *

# Brother vs. Brother

def GetAbilities() -> Sequence['Ability']:

    def brother_vs_brother(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        from game.player import Player

        attacker = message.attacker
        if not Player.IsType(attacker.GetControlBy()):
            return

        player = attacker.GetControlByPlayer()
        if not CostFunc.Discard("YourHandCards").PayCost(effect, player):
            message.SetBeInstead(effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "Player",
            CardFinder(name="Grim Reaper"),
            brother_vs_brother,
        ),
    ]