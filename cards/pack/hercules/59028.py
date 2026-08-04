from . import *

# * Evaluate Threat

def GetAbilities() -> Sequence['Ability']:

    def evaluate_threat(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        def action(player: 'Player'):
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                include_discard_pile=True,
                may=True,
                traits=["AVENGER", "S.H.I.E.L.D"],
            )
            if face:
                player.GainCard(face, effect)
                Worlds.UpdateNextCardPlayCost(
                    player,
                    -2,
                    effect,
                    finder=CardFinder(
                        check_face_fn=lambda check_face, selected_face=face:
                            check_face == selected_face
                    ),
                    in_this="Phase"
                )

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.CanPlayThisSchemeCard(
            conditions=[
                lambda effect, message:
                    effect.GetInitiator().GetIdentity().HasTrait("AVENGER", "S.H.I.E.L.D")
            ]
        ).SetPlay(),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            evaluate_threat,
        ),
    ]
