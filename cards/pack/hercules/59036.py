from . import *

# * Ares

def GetAbilities() -> Sequence['Ability']:

    def ares_schemes(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        effect.GetInitiator().DealEncounterCards(1, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1,
            retaliate=1,
        ),
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            ares_schemes,
        ),
    ]
