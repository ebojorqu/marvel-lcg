from . import *

# Pacifism

def GetAbilities() -> Sequence['Ability']:

    def can_discard_three_tucked_under_ionic_physiology(effect: 'Effect', message: 'Message2') -> bool:
        Unused(message)

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
        return len(tucked) >= 3

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

    action_exhaust = AbilityFactory.WhenInYourPlayTurn(
        AbilityType.AlterEgoAction,
        discard_this,
    ).SetName("Exhaust Simon Williams").SetCostFunc(CostFunc.Exhaust(name="Simon Williams"))

    action_discard_three = AbilityFactory.WhenInYourPlayTurn(
        AbilityType.AlterEgoAction,
        discard_this,
    ).SetName("discard 3 cards tucked under ionic physiology")
    action_discard_three.SetCostFunc(CostFunc.Custom(None, discard_three_tucked_under_ionic_physiology))
    action_discard_three.conditions = [can_discard_three_tucked_under_ionic_physiology] + action_discard_three.conditions

    return [
        *AbilityFactory.UnitCannotAttackTarget(
            "AttachedIdentity",
            cannot_attack=True,
            cannot_trigger_attack_ability=True,
        ),
        action_exhaust,
        action_discard_three,
    ]