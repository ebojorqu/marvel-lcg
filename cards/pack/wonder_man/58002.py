from . import *

# Ionic Physiology

def GetAbilities() -> Sequence['Ability']:

    def ionic_physiology(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        played_event = message.played_face
        player = effect.GetInitiator()

        if played_event.card.area != player.discard_pile:
            return

        this.TuckCardUnderHere([played_event], effect)
        this.HealthUnits([player.GetIdentity()], 1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(card_type=Event, has_printed_res="Y"),
            ionic_physiology,
            conditions=[
                lambda effect, message:
                    effect.this.GetPlacedCardArea().GetSize() < 3,
            ],
        ),
    ]