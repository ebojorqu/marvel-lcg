from . import *

# God of War

def GetAbilities() -> Sequence['Ability']:

    def god_of_war(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        did_attack = False

        for player in Players.GetAll(effect):
            for minion in player.GetEngagedMinions():
                did_attack = True
                minion.BasicAttack([player.GetIdentity()], effect)

        if not did_attack:
            minion = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
            if minion:
                minion.Reveal(effect.GetInitiator(), effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            god_of_war,
        ),
    ]
