from . import *

# * Hercules (Hero)

def GetAbilities() -> Sequence['Ability']:

    def atonement(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        player = this.GetControlByPlayer()
        gift = GetTopGiftCard(player)
        if gift:
            gift.PutIntoPlay(player, effect)

        Faces.ReadyAll([this], effect)
        YouMayFlipToYourAlterEgoForm(player, effect)

    def labor_added_to_victory_display(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        this = effect.this.CastTo(Hero)
        if not this.IsInPlay():
            return False
        for face in message.faces:
            if face.card.area == effect.world.victory_display and face.paper.card_id in LABOR_CARD_IDS:
                return True
        return False

    return [
        AbilityFactory.AfterCardsMoved(
            AbilityType.Response,
            None,
            atonement,
            conditions=[labor_added_to_victory_display],
        ).SetName("Atonement").LimitOncePerPhase(),
    ]
