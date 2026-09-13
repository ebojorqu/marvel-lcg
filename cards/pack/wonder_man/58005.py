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

        # Card cost is 1: if all paid resources are energy, one energy may be used
        # to satisfy base cost and is not overpaid.
        if paid.val > paid_energy:
            overpaid_energy = paid_energy
        else:
            overpaid_energy = max(0, paid_energy - 1)

        if overpaid_energy > 0:
            Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            starstruck
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]