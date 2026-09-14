from . import *

# Energy Siphon

def GetAbilities() -> Sequence['Ability']:

    def energy_siphon_check(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()
        if not initiator.IsHero():
            return Resources("Y")

        # Base 1 [energy] plus up to 3 from this card's effect.
        return Resources("Y") * 4

    def energy_siphon_res(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)

        initiator = effect.GetInitiator()
        if not initiator.IsHero():
            return Resources("Y")

        identity = initiator.GetIdentity()

        damage = initiator.DeclareNumber(0, 3)
        if damage <= 0:
            return Resources("Y")

        damage_message = identity.TakeDamage(this, damage, effect)
        if not damage_message or damage_message.took_damage <= 0:
            return Resources("Y")

        return Resources("Y") * (1 + damage_message.took_damage)

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(
            AbilityType.DiscardForResource,
            res_fn=energy_siphon_res,
        ),
        AbilityFactory.CheckThisCanDropPay(
            energy_siphon_check,
        ),
    ]