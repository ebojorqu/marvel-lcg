from . import *

# Herc's Helm

def GetAbilities() -> Sequence['Ability']:

    def hercs_helm(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        would_atk_message = message

        def reduce_this_attack_damage(reduce_effect: 'Effect', damage_message: 'Message.WhenUnitWouldTakeDamage') -> None:
            damage_message.PreventDamage(1, reduce_effect)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                None,
                reduce_this_attack_damage,
                conditions=[
                    lambda reduce_effect, damage_message: damage_message.would_atk_message == would_atk_message,
                ],
            ),
            unregister_after_exec=True,
            until_event_end=would_atk_message,
        )

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.HeroInterrupt,
            Villain,
            hercs_helm,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetLabel("defense").SetCostFunc(CostFunc.Exhaust("This")),
    ]
