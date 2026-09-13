from . import *

# Jet Belt

def GetAbilities() -> Sequence['Ability']:

    def has_tucked_under_ionic_physiology(effect: 'Effect') -> bool:
        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )
        if not ionic_physiology:
            return False
        return ionic_physiology.GetPlacedCardArea().GetSize() > 0

    def discard_tucked_under_ionic_physiology(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)

        if not has_tucked_under_ionic_physiology(effect):
            return False

        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )
        assert ionic_physiology

        tucked = ionic_physiology.GetPlacedCardArea().GetAll()

        discarded = initiator.AskDiscardFaces(tucked, (1, 1), effect)
        return len(discarded) == 1

    def check_can_generate(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        paying_for_card = message.paying_for_card
        if paying_for_card and Event.IsType(paying_for_card):
            return True
        return has_tucked_under_ionic_physiology(effect)

    def discard_if_not_event(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)

        paying_message = effect.GetBindMessage(Message.WhenPlayerPayingResources)
        paying_for_card = paying_message.for_effect.this
        if Event.IsType(paying_for_card):
            return True
        return discard_tucked_under_ionic_physiology([], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
            conditions=[check_can_generate],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, discard_if_not_event)),
    ]