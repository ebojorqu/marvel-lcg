from . import *

# Cameo

def GetAbilities() -> Sequence['Ability']:

    def cameo(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        from cards.paper import Paper

        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()

        def check_ally(paper: 'Paper') -> bool:
            # Identity-specific allies use set_name to identify the linked hero identity.
            if paper.set_name == "":
                return False
            return not any(player.IsName(paper.set_name) for player in Worlds.GetPlayers(effect))

        ally = Search.Collection(
            effect,
            initiator,
            card_type=Ally,
            card_class="IdentitySpecific",
            check_fn=check_ally,
        )

        if ally:
            Faces.ShuffleAllTo([ally], initiator.player_deck, effect)
        
        initiator.DiscardHandCards((2, 2), effect)
        Faces.RemoveAllFromGame([this], effect)


    return [
        AbilityFactory.WhenCardSetup(
            "This",
            cameo
        ),
    ]

