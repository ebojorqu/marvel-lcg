from . import *

# Mutagen Cloud - 2B

def GetAbilities() -> Sequence['Ability']:

    def mutagen_cloud(effect: 'Effect') -> int:
        from engine.log import Notify

        this = effect.this.CastTo(MainScheme)
        Unused(this)

        value = 0
        green_goblin_count = 0
        goblin_minion_count = 0

        villain = Worlds.FindVillain(effect)
        if villain and villain.IsInPlay() and villain.IsName("Green Goblin", check_all_face=True):
            green_goblin_count = 1
            value += 1

        for minion in Worlds.GetOnFieldMinions(effect):
            if minion.HasTrait("GOBLIN"):
                goblin_minion_count += 1
                value += 1

        Notify.Game(f"Mutagen Cloud X={value} (Green Goblin={green_goblin_count}, Goblin Minions={goblin_minion_count})")

        return value


    return [
        AbilityFactory.WhenCalcThisSchemeEscalation(
            mutagen_cloud
        ),
    ]

