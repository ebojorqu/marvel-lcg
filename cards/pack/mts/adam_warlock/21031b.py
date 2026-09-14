from . import *

# * Adam Warlock

def GetAbilities() -> Sequence['Ability']:

    def adam_warlock(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        Faces.DiscardAll(effect.targets, effect)


    return [
        # <i>Avatar of Life</i> - During deck-building, your deck must include an equal number of cards from all 4 aspects. You cannot include more than 1 copy of any non-Adam Warlock card.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            adam_warlock
        ).SetCostFunc(CostFunc.Discard("YourHandCards"))
        # Match status cards attached to this identity card across either face.
        .SetTarget(
            StatusCard,
            canbe_discard=True,
            check_fn=lambda effect, face: face.GetBindFace().card == effect.this.card,
        ),
    ]

