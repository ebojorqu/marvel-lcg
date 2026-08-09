from . import *

# * Shield of Perseus

def GetAbilities() -> Sequence['Ability']:

    def draw_cards(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        effect.GetInitiator().DrawUp(4, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached("You", health=1, retaliate=1),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Response,
            "This",
            draw_cards,
        ),
    ]
