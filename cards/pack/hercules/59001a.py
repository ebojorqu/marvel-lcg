from . import *

# * Hercules (Hero)

def GetAbilities() -> Sequence['Ability']:

    def atonement(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        player = effect.GetInitiator()
        gift = GetTopGiftCard(player)
        if gift:
            gift.PutIntoPlay(player, effect)

        Faces.ReadyAll([this], effect)
        YouMayFlipToYourAlterEgoForm(player, effect)

    def labor_entered_victory(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        if not effect.GetInitiator().form.IsInHeroForm():
            return False
        if not any(x.flags.is_victory_display for x in message.into_areas):
            return False
        return message.IsIncludeFace(CardFinder(trait="LABOR"), effect) is not None

    return [
        AbilityFactory.AfterCardsMoved(
            AbilityType.Response,
            "AnyCard",
            atonement,
            conditions=[labor_entered_victory],
        ).SetName("Atonement").LimitOncePerPhase(),
    ]
