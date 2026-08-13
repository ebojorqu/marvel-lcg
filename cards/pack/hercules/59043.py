from . import *

# * Kyknos

def GetAbilities() -> Sequence['Ability']:

    def kyknos_activates(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        scheme = Worlds.FindCardOnField(effect, name=ALL_VERSUS_ALL, card_type=SchemeSide2)
        if scheme:
            scheme.PlaceThreatOnSchemes([scheme], 2, effect)
        else:
            main_scheme = Worlds.GetMainScheme(effect)
            main_scheme.PlaceThreatOnSchemes([main_scheme], 1, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "This",
            kyknos_activates,
        ),
    ]
