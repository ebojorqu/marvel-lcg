from . import *

# * Hercules (Alter-Ego)

def GetAbilities() -> Sequence['Ability']:

    def setup_hercules(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        player = effect.GetInitiator()
        faces = list(player.set_aside_deck.Get())

        labor_faces = [x for x in faces if x.paper.card_id in LABOR_CARD_IDS]
        gift_faces = [x for x in faces if x.paper.card_id in GIFT_CARD_IDS]

        if labor_faces:
            Faces.ShuffleAllTo(labor_faces, player.additional_deck, effect)
        if gift_faces:
            Faces.ShuffleAllTo(gift_faces, player.set_aside_deck, effect)
            Faces.FlipAllTo(gift_faces, False, effect)

    def new_labors_of_hercules(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        player = effect.GetInitiator()
        labor = GetTopLaborCard(player)
        if labor:
            labor.Reveal(player, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(
            [
                *LABOR_CARD_IDS,
                *GIFT_CARD_IDS,
            ],
            setup_hercules,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            new_labors_of_hercules,
            conditions=[
                lambda effect, message: effect.GetInitiator().IsAlterEgo(),
                lambda effect, message: not Worlds.FindCardOnField(effect, trait="LABOR"),
                lambda effect, message: GetTopLaborCard(effect.GetInitiator()) is not None,
            ],
        ).SetName("New Labors of Hercules"),
    ]
