from . import *

# Avengers Compound

def GetAbilities() -> Sequence['Ability']:

    def tuck_ally(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        this.TuckCardUnderHere(effect.targets, effect, peek=True)

    def play_tucked_ally(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.PlayCardsLikeInTurn(
            effect.targets,
            effect,
            forced=False,
            if_not_play_discard_it=False,
        )

    return [
        AbilityFactory.CanPlayThisSupportCard(
        ).SetPlay(only_if_your_identity_has_trait="AVENGER"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            tuck_ally,
            conditions=[
                lambda effect, message:
                    effect.this.GetPlacedCardArea().GetSize() == 0
            ]
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Ally, from_where=["YourHandCards"]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            play_tucked_ally,
            conditions=[
                lambda effect, message:
                    effect.this.GetPlacedCardArea().GetSize() > 0
            ]
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("TuckHereCard", card_type=Ally),
    ]
