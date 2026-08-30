from . import *

# The Best Offense...

def GetAbilities() -> Sequence['Ability']:

    def the_best_offense(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        hero = this.bind_face or message.trigger
        if not hero:
            return

        if message.power == "ATK":
            current_value = hero.attack
        elif message.power == "THW":
            current_value = hero.thwart
        else:
            return

        message.GainValue(hero.defense - current_value, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            defense=1,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            the_best_offense,
            powers=["ATK", "THW"],
            conditions=[
                lambda effect, message:
                    effect.this.bind_face == message.trigger
            ],
        ).SetTarget("Trigger")
    ]
