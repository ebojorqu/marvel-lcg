from . import *

# Stand Alone

def GetAbilities() -> Sequence['Ability']:

    def stand_alone(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        this.Exhaust(effect)
        Faces.ReadyAll([hero], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            stand_alone,
            against_player="You",
            conditions=[
                lambda effect, message:
                    len(effect.GetInitiator().GetControlCards(CardFinder(card_type=Ally))) == 0
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
    ]
