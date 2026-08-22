from . import *

# * Teddy Altman

def GetAbilities() -> Sequence['Ability']:

    def no_second_shapeshift(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> bool:
        owner = message.trigger.GetOwner()
        if not isinstance(owner, Player):
            return False
        return owner.GetControlCards2(CardFinder2("SHAPESHIFT", Upgrade)) != []

    def teddy_altman(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="SHAPESHIFT",
            card_type=Upgrade
        )
        if face:
            Faces.AddToHand([face], initiator, effect)


    return [
        AbilityFactory.WhenCardWouldMoveToArea(
            AbilityType.NonKeyword,
            CardFinder(trait="SHAPESHIFT", card_type=Upgrade),
            lambda effect, message:
                message.SetCannot(effect),
            into_play=True,
            conditions=[
                no_second_shapeshift,
            ]
        ).SetName("You cannot have more than 1 Shapeshift upgrade in play."),
        AbilityFactory.PlayersCannotPlayCardWhile(
            "You",
            CardFinder2("SHAPESHIFT", Upgrade),
            conditions=[
                lambda effect, message:
                    effect.GetInitiator().GetControlCards2(CardFinder2("SHAPESHIFT", Upgrade)) != []
            ]
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            teddy_altman
        ).SetName("Shape-Changer")
        .LimitOncePerRound(),
    ]

