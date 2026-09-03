from . import *
from cards.pack.sm.campaign import *

# "Leave Us Alone!"

def GetAbilities() -> Sequence['Ability']:

    def leave_us_alone(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        SetupCards.PutIntoPlay(
            effect,
            finder=CardFinder(card_ids=["27077a", "27077b"]),
            card_type=Environment,
            from_where=["SetAside"],
            flip_to_trait="QUIET",
        )

    def campaign_expert(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            PlaceFaceDownBoostCardsOnPlayer(player, 1, effect)

    return [
        *CampaignSetup(2, campaign_expert=campaign_expert),
        AbilityFactory.WhenCardSetup(
            "This",
            leave_us_alone
        ),
    ]

