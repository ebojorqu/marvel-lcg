from . import *

# Protect Humanity

def GetAbilities() -> Sequence['Ability']:

    def protect_humanity_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        cho = Search.PlayerCard(
            effect,
            effect.GetInitiator(),
            include_player_deck=True,
            include_discard_pile=True,
            include_player_hand_cards=True,
            include_player_area=True,
            name="Amadeus Cho",
            card_type=Ally,
            not_move=True,
        )
        if cho:
            cho.PutIntoPlay(effect.GetInitiator(), effect)

    def redirect_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        player = effect.GetInitiator()
        allies = player.GetControlAllies()
        if not allies:
            return

        ally = player.AskChooseFace(allies, effect)
        if ally:
            message.ChangeTarget(ally, effect)

        def after_attack() -> None:
            if message.would_atk_message.defender and message.would_atk_message.defender.IsName("Hercules"):
                Faces.RemoveCountersOn([this], 1, "labor", effect)

        message.AfterThisAttack(after_attack)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            protect_humanity_revealed,
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            Villain,
            Hero,
            redirect_attack,
            conditions=[
                lambda effect, message: effect.this.IsInPlay(),
                lambda effect, message: message.attacked[0].IsName("Hercules"),
            ],
        ).NoOutOfPlayLimit(),
    ]
