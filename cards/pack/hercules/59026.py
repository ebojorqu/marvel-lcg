from . import *

# Ancient Rivalry

def GetAbilities() -> Sequence['Ability']:

    def ancient_rivalry(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()

        card = Search.PlayerCard(
            effect,
            player,
            include_player_deck=False,
            include_discard_pile=True,
            card_type=Upgrade,
            card_class="IdentitySpecific",
            may=True,
        )
        if card:
            player.GainCard(card, effect)

        for check_player in Players.GetAll(effect):
            identity = check_player.GetIdentity()
            if identity.IsName("Hercules", "Thor"):
                Faces.ReadyAll([identity], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ancient_rivalry,
        ).SetPlay().SetTarget("TeamUp"),
    ]
