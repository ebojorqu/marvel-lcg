from . import *

# Death Cannot Die

def GetAbilities() -> Sequence['Ability']:

    def death_cannot_die_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        grim_reaper = Worlds.FindCardOnField(
            effect,
            name="Grim Reaper",
            card_type=Minion,
        )
        if grim_reaper:
            grim_reaper.DoActivate(player, effect)
            return

        grim_reaper = Search.EncounterCard(
            effect,
            include_discard_pile=True,
            name="Grim Reaper",
            card_type=Minion,
        )
        if grim_reaper:
            grim_reaper.Reveal(player, effect)

    def death_cannot_die_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        grim_reaper = Worlds.FindCardOnField(
            effect,
            name="Grim Reaper",
            card_type=Minion,
        )
        if not grim_reaper:
            return

        player = message.GetToPlayer()
        message.AfterThisActivation(
            effect,
            lambda: grim_reaper.DoActivate(player, effect),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            death_cannot_die_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            death_cannot_die_boost,
        ),
    ]