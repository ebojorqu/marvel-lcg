from . import *

# Disarming Defense

def GetAbilities() -> Sequence['Ability']:

    def disarming_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        message.GainDEFForThisAttack(+2, effect)

        def action():
            if message.attacker:
                Players.DiscardHeroActionAttachment(initiator, [message.attacker], effect, may=False)
        message.IfYouTakeNoDamage(action)


    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            disarming_defense,
            against_who=Enemy,
        ).SetPlay().SetLabel('defense'),
    ]

