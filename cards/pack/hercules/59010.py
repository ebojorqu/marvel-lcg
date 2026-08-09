from . import *

# Son of Zeus

def GetAbilities() -> Sequence['Ability']:

    def son_of_zeus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()
        hero = player.GetHero()
        Faces.ReadyAll([hero], effect)

        gifts = GetGiftCount(player)

        if gifts >= 1:
            upgrade = player.AskChooseFace(
                player.GetControlCards(CardFinder(card_type=Upgrade, card_class="IdentitySpecific", canbe_ready=True)),
                effect,
            )
            if upgrade:
                Faces.ReadyAll([upgrade], effect)

        if gifts >= 2:
            Faces.GiveStatus([hero], "Tough", effect)

        if gifts >= 3:
            player.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            son_of_zeus,
        ).SetPlay(),
    ]
