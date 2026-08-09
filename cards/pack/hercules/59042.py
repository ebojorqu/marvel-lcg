from . import *

# * Hecate

def GetAbilities() -> Sequence['Ability']:

    def reveal_all_versus_all(effect: 'Effect', message: 'Message.WhenCardRevealed|Message.WhenUnitBeDefeated') -> None:
        RevealAllVersusAll(effect, effect.GetInitiator())

    def hecate_activates(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        scheme = Worlds.FindCardOnField(effect, name=ALL_VERSUS_ALL, card_type=SchemeSide2)
        if scheme:
            scheme.PlaceThreat(2, effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            reveal_all_versus_all,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedResponse,
            "This",
            reveal_all_versus_all,
        ),
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            hecate_activates,
        ),
    ]
