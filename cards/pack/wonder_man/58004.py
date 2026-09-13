from . import *

# Ionic Blast

def GetAbilities() -> Sequence['Ability']:

    def ionic_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        paid = effect.GetPaidResources()
        paid_energy = paid.GetColor("Y")

        # Card cost is 1: if all paid resources are energy, one energy may be used
        # to satisfy base cost and is not overpaid.
        if paid.val > paid_energy:
            overpaid_energy = paid_energy
        else:
            overpaid_energy = max(0, paid_energy - 1)

        overpaid_energy = min(3, overpaid_energy)
        value = 3 + overpaid_energy * 2
        this.DealDamage(effect.targets, value, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ionic_blast
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]