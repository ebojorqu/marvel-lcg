from . import *

# Jarvis

def GetAbilities() -> Sequence['Ability']:

    def jarvis(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        identity = message.trigger.CastTo(Identity)
        affected_player = identity.GetControlByPlayer()

        def gain_rec_until_phase_end(targets: Sequence['CardFace']):
            target = targets[0].CastTo(Identity)
            target.TemporaryGain(
                effect,
                None,
                Message.WhenPhaseEnd,
                recover=2,
            )

        choices: List[Ability] = [
            AbilityFactory.ForChoiceAbility(
                "That identity gets +2 REC until the end of the phase",
                gain_rec_until_phase_end,
            ).SetTarget([identity]),
        ]

        if identity.GetStatusSize() > 0:
            choices.append(
                AbilityFactory.ForChoiceAbility(
                    "Discard a status card from that identity",
                    lambda targets:
                        Faces.DiscardAll(targets, effect),
                ).SetTarget(StatusCard, bind_to=identity, canbe_discard=True)
            )

        affected_player.ChooseAbilities(effect, *choices)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            CardFinder(trait="AVENGER"),
            jarvis,
            from_form=Hero,
            to_form=AlterEgo,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]