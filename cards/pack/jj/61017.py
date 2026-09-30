from . import *

# * Squirrel Girl: Doreen Green

def GetAbilities() -> Sequence['Ability']:

    def squirrel_girl_response(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        counters = min(4, player.hand_cards.GetSize())
        if counters:
            Faces.PlaceCountersOn([this], counters, 'squirrel', effect, maximum=4)

    def squirrel_girl_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.Response,
            squirrel_girl_response,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            squirrel_girl_action,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'squirrel'))
        .SetTarget(Scheme2),
    ]