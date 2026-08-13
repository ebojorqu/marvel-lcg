from . import *

# Son of Zeus

def GetAbilities() -> Sequence['Ability']:

    def can_resolve_son_of_zeus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        player = effect.GetInitiator()
        hero = player.GetHero()
        gifts = GetGiftCount(player)

        if hero.CanReady():
            return True

        if gifts >= 1:
            readyable_upgrades = player.GetControlCards(
                CardFinder(card_type=Upgrade, card_class="IdentitySpecific", canbe_ready=True)
            )
            if readyable_upgrades:
                return True

        if gifts >= 2 and hero.CanGainTough():
            return True

        if gifts >= 3:
            return True

        return False

    def son_of_zeus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()
        hero = player.GetHero()

        if hero.CanReady():
            Faces.ReadyAll([hero], effect)

        gifts = GetGiftCount(player)

        if gifts >= 1:
            readyable_upgrades = player.GetControlCards(
                CardFinder(card_type=Upgrade, card_class="IdentitySpecific", canbe_ready=True)
            )
            if readyable_upgrades:
                upgrade = player.AskChooseFace(
                    readyable_upgrades,
                    effect,
                )
                if upgrade:
                    Faces.ReadyAll([upgrade], effect)

        if gifts >= 2 and hero.CanGainTough():
            Faces.GiveStatus([hero], "Tough", effect)

        if gifts >= 3:
            player.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            son_of_zeus,
            conditions=[
                can_resolve_son_of_zeus,
            ],
        ).SetPlay(),
    ]
