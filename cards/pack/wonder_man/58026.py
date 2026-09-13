from . import *

# * Grim Reaper

def GetAbilities() -> Sequence['Ability']:

    def grim_reaper(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.target.GetControlByPlayer()
        player.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            "This",
            Ally,
            grim_reaper,
            is_from_attack=True,
        ),
    ]