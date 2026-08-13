from . import *

# * Lernean Hydra

def GetAbilities() -> Sequence['Ability']:

    def lernean_hydra(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        dealt_to_hydra = sum(
            x.dealt_damage
            for x in message.atk_messages
            if x.attacked == effect.this
        )
        if dealt_to_hydra <= 0:
            return

        player = message.attacker.GetControlByPlayer()

        pay_effect = player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("R"),
                "Spend a physical resource",
                lambda targets, resources: None,
            ),
        )

        if not pay_effect:
            effect.this.CastTo(Minion).HealHealth(2, effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            Friend,
            lernean_hydra,
            conditions=[
                lambda effect, message: effect.this.IsInPlay(),
                lambda effect, message: any(x.attacked == effect.this for x in message.atk_messages),
            ],
        ).NoOutOfPlayLimit(),
    ]
