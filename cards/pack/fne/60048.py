from . import *

# Army of One

def GetAbilities() -> Sequence['Ability']:

    def army_of_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        Faces.ReadyAll([hero], effect)


    return [
        AbilityFactory.UpdateCostOfCardInternal(
            "This",
            lambda effect: len(effect.GetInitiator().GetControlCards(CardFinder(card_type=Ally))),
            "You",
            is_play=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            army_of_one,
            conditions=[
                lambda effect, message: not effect.GetInitiator().GetHero().IsReady(),
            ],
        ).SetPlay().SetLabel(),
    ]
