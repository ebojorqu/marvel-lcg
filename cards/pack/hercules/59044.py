from . import *

# Bewitched Officer

def GetAbilities() -> Sequence['Ability']:

    def bewitched_officer_attack_keywords(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)
        message.GainRanged(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            bewitched_officer_attack_keywords,
            conditions=[
                lambda effect, message: message.IsBasicAttack(),
            ],
        ),
    ]
