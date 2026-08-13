from . import *

# Appeal to Athena

def GetAbilities() -> Sequence['Ability']:

    def appeal_to_athena(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()
        this = effect.this.CastTo(Obligation)
        Unused(this)

        def exhaust_identity_and_remove(targets: Sequence['CardFace']) -> None:
            if Faces.ExhaustAll(targets, effect) == list(targets):
                Faces.RemoveAllFromGame([effect.this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("BB"),
                "Spend 2 mental resources",
                lambda targets, resources:
                    Faces.RemoveAllFromGame([effect.this], effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity",
                exhaust_identity_and_remove,
            ).SetTarget("YourIdentity", canbe_exhaust=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            appeal_to_athena,
            conditions=[
                lambda effect, message: effect.GetInitiator().IsAlterEgo(),
            ],
        ),
    ]
