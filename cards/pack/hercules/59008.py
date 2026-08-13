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

        if not Minion.IsType(message.attacker):
            return

        target = message.target
        player = this.GetControlByPlayer()
        if target.GetControlByPlayer() != player:
            return
        if not (Hero.IsType(target) or AlterEgo.IsType(target)):
            return

        message.ChangeTarget(this, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            amadeus_cho_draw,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            Minion,
            "YourIdentity",
            amadeus_cho_redirect,
        ).NoOutOfPlayLimit(),
    ]
