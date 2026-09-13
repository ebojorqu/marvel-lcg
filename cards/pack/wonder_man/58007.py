from . import *

# Wonder Fans

def GetAbilities() -> Sequence['Ability']:

    def wonder_fans(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Tuck 1 event with a printed [energy] resource under Ionic Physiology",
                lambda targets:
                    ionic_physiology.TuckCardUnderHere(targets, effect)
            ).SetTarget(
                Event,
                has_printed_res="Y",
                from_where=["YourDiscardPile"],
            ) if ionic_physiology and ionic_physiology.GetPlacedCardArea().GetSize() < 3 else None,
            AbilityFactory.ForChoiceAbility(
                "Draw 1 card",
                lambda targets:
                    initiator.DrawUp(1, effect)
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            wonder_fans
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]