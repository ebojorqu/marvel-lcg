from . import *

# Signature Sunglasses

def GetAbilities() -> Sequence['Ability']:

    def signature_sunglasses(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )
        if ionic_physiology is None:
            return

        discard_events = initiator.discard_pile.FindCards(card_type=Event, has_printed_res="Y")
        discard_resources = initiator.discard_pile.FindCards(card_type=Resource, has_printed_res="Y")
        can_tuck_from_discard = discard_events + discard_resources
        tucked_cards = ionic_physiology.GetPlacedCardArea().Get()

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Tuck an event or resource card with a printed [energy] resource from your discard pile under Ionic Physiology",
                lambda targets:
                    ionic_physiology.TuckCardUnderHere(targets, effect)
            ).SetTarget(can_tuck_from_discard)
            if ionic_physiology.GetPlacedCardArea().GetSize() < 3 and can_tuck_from_discard else None,
            AbilityFactory.ForChoiceAbility(
                "Add a card tucked under Ionic Physiology to your hand",
                lambda targets:
                    initiator.GainCard(targets, effect)
            ).SetTarget(tucked_cards)
            if tucked_cards else None,
        )

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            signature_sunglasses,
        ),
    ]