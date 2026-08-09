from . import *

# * Amadeus Cho

def GetAbilities() -> Sequence['Ability']:

    def amadeus_cho_draw(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        effect.GetInitiator().DrawUp(1, effect)

    def amadeus_cho_redirect(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        if not this.IsInPlay():
            return

        if not message.attacker.IsMinion():
            return

        target = message.target
        player = this.GetControlByPlayer()
        if target != player.GetIdentity():
            return

        message.ChangeTarget(this, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            amadeus_cho_draw,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            Enemy,
            "YouControlUnit",
            amadeus_cho_redirect,
        ).NoOutOfPlayLimit(),
    ]
