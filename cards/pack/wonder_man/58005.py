from . import *

# Starstruck

def GetAbilities() -> Sequence['Ability']:

    def starstruck(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        value = initiator.GetHero().attack
        this.DealDamage(effect.targets, value, effect)

        paid = effect.GetPaidResources()
        paid_energy = paid.GetColor("Y")

        # Determine how much Y actually counts as overpay after final cost modifiers.
        # For generic costs, non-Y can satisfy cost first; only remaining needed cost
        # can consume Y. Any extra Y beyond that is true overpay.
        final_cost = effect.context.paid_this_cost.true_val
        paid_non_energy = paid.val - paid_energy
        energy_used_for_cost = max(0, final_cost - paid_non_energy)
        energy_used_for_cost = min(energy_used_for_cost, paid_energy)
        overpaid_energy = max(0, paid_energy - energy_used_for_cost)

        if overpaid_energy > 0:
            Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            starstruck
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]