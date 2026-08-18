from . import *
from cards.pack.mojo import DiscardEachSettingAndGainSurge

# Wild Wild Mojo

def GetAbilities() -> Sequence['Ability']:

    def wild_wild_mojo(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Environment)
        Unused(this)

        if message.IsOverkill():
            message.property.damage += 1
            Message.WhenDamageUpdated_Text(1, effect)
        else:
            message.IncreaseDamage(1, effect)


    return [
        AbilityFactory.UnitAttackGainKeyword(
            Enemy,
            overkill=True
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            None,
            wild_wild_mojo,
            # include_overkill=False
        ),
        DiscardEachSettingAndGainSurge()
    ]

