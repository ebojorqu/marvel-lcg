from . import *

# * Lernean Hydra

def GetAbilities() -> Sequence['Ability']:

    # Prevented damage doesn't count, so use `taken_damage` instead of `dealt_damage`
    def damage_taken_from_attack(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> int:
        return sum(
            x.taken_damage
            for x in message.atk_messages
            if x.attacked == effect.this
        )

    def lernean_hydra(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
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
                lambda effect, message: damage_taken_from_attack(effect, message) > 0,
            ],
        ).NoOutOfPlayLimit(),
    ]
