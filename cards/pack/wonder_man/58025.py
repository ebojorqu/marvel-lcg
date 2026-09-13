from . import *

# Pacifism

def GetAbilities() -> Sequence['Ability']:

    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        Faces.DiscardAll([this], effect)

    def discard_three_tucked_under_ionic_physiology(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)

        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )
        if not ionic_physiology:
            return False

        tucked = ionic_physiology.GetPlacedCardArea().GetAll()
        if len(tucked) < 3:
            return False

        discarded = initiator.AskDiscardFaces(tucked, (3, 3), effect)
        return len(discarded) == 3

    return [
        *AbilityFactory.UnitCannotAttackTarget(
            "AttachedIdentity",
            cannot_attack=True,
            cannot_trigger_attack_ability=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            discard_this,
        ).SetCostFunc(CostFunc.Exhaust(name="Simon Williams")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            discard_this,
        ).SetCostFunc(CostFunc.Custom(None, discard_three_tucked_under_ionic_physiology)),
    ]