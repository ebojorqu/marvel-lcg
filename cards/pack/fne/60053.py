from . import *

# Ronin

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=lambda effect, attach, ui: 1 if len(attach.GetControlByOrOwner().GetControlCards(CardFinder(card_type=Ally))) == 0 else 0,
            defense=1,
            retaliate=1,
            ex_change_on_event=OnEvent.PlayAreaCard("YouControlCards")
        )
    ]
