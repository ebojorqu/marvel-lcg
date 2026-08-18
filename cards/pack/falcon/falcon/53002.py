from . import *

# * Redwing

def GetAbilities() -> Sequence['Ability']:

    def redwing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        faces = effect.cost_func.Get(CostFunc.DiscardDeckTopCards).return_discarded_cards
        value = FacesCounter.CountTotalBoostStarAndBoost(faces)

        this.DealDamage(effect.targets, value, effect)
        this.RemoveThreatFromSchemes(effect.targets, value, effect)

    def redwing_condition(effect: 'Effect', face: 'CardFace') -> bool:
        if Scheme2.IsReallyType(face):
            return face.threat > 0
        if Enemy.IsReallyType(face):
            return face.health > 0
        return False

    def redwing_has_known_boost_value(effect: 'Effect', message: 'Message2') -> bool:
        encounter_deck = Worlds.GetEncounterDeck(effect)
        top_card = encounter_deck.GetTop()
        if top_card is None:
            return False
        if top_card.IsFaceUp():
            return FacesCounter.CountTotalBoostStarAndBoost([top_card]) > 0
        return True

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redwing,
            conditions=[redwing_has_known_boost_value]
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.ReturnToHand("This", to_who="Initiator"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("EncounterDeck", 1))
        .SetTarget("Enemy|Scheme", check_fn=redwing_condition)
    ]

