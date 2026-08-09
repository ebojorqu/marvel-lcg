from . import *

# * Sword of Peleus

def GetAbilities() -> Sequence['Ability']:

    def draw_cards(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        effect.GetInitiator().DrawUp(4, effect)

    def gain_piercing(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)

    return [
        *AbilityFactory.GiveKeywordToAttached("You", health=1),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.NonKeyword,
            "You",
            gain_piercing,
            is_basic_attack=True,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).NoOutOfPlayLimit(),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Response,
            "This",
            draw_cards,
        ),
    ]
