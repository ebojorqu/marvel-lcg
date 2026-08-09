from . import *

# All Versus All

def GetAbilities() -> Sequence['Ability']:

    def all_versus_all_gain_threat(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        effect.this.CastTo(SchemeSide2).PlaceThreat(2, effect)

    def all_versus_all_set_aside(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Faces.SetAside([effect.this], effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedResponse,
            "AnyCard",
            all_versus_all_gain_threat,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).NoOutOfPlayLimit(),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            all_versus_all_set_aside,
        ),
    ]
