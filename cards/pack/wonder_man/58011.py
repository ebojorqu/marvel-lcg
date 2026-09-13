from . import *

# "What Are You?"

def GetAbilities() -> Sequence['Ability']:

    def what_are_you(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)

        wonder_man = message.trigger.CastTo(Identity)
        message.SetBeInstead(effect)

        wonder_man.SetHealth(4, effect)
        wonder_man.ChangeToForm(AlterEgo, effect)

        initiator = effect.GetInitiator()
        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
            owner=initiator,
        )
        if ionic_physiology:
            need = 3 - ionic_physiology.GetPlacedCardArea().GetSize()
            if need > 0:
                faces = initiator.discard_pile.FindCards(card_type=Event, has_printed_res="Y")
                choose = initiator.AskChooseFaces(
                    faces,
                    (0, need),
                    effect,
                    prompt="Tuck events under Ionic Physiology",
                    peek=True,
                    not_move=True,
                )
                if choose:
                    ionic_physiology.TuckCardUnderHere(choose, effect)

        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Wonder Man"),
            what_are_you,
        )
    ]