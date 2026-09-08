from . import *

# * Enchantress

def GetAbilities() -> Sequence['Ability']:

    def enchantress_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterVillain)
        Unused(this)

        if Worlds.IsStandard(effect):
            face = SetupCards.PutIntoPlay(
                effect,
                finder=CardFinder(card_ids=["55006"]),
                from_where=["SetAside"],
            )

            if face:
                this.PlaceThreatOnSchemes([face], "3*", effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            enchantress_revealed
        ),
        AfterEnchantressAttacksYouPlaceCharmCounter(),
    ]

