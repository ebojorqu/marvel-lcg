from . import *

# Hex Bolt

def GetAbilities() -> Sequence['Ability']:

    def hex_bolt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        discarded_faces = Worlds.DiscardEncounterCards(3, effect)
        resolving_faces = list(discarded_faces)
        Message.TextRender(
            f"Hex Bolt: resolving {len(resolving_faces)} discarded card(s)",
            effect.world,
        )

        # Keep the discarded set visible during resolution, even if the deck reset
        # moved some of these cards back into the encounter deck.
        Faces.LookAt(resolving_faces, initiator, effect)

        for face in resolving_faces:
            boost_icons = FacesCounter.CountTotalBoostIcons([face])
            if boost_icons == 0:
                initiator.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "",
                        lambda targets:
                            this.DealDamage(targets, 2, effect)
                    ).SetTarget(Enemy)
                )
            elif boost_icons == 1:
                initiator.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "",
                        lambda targets:
                            this.RemoveThreatFromSchemes(targets, 2, effect)
                    ).SetTarget(Scheme2)
                )
            elif boost_icons == 2:
                initiator.DrawUp(1, effect)
            elif boost_icons >= 3:
                status = initiator.DeclareStatusCard()
                if status:
                    the_status: CardFace.STATUS = status
                    initiator.ChooseAbilities(
                        effect,
                        AbilityFactory.ForChoiceAbility(
                            "",
                            lambda targets:
                                Faces.GiveStatus(targets, the_status, effect)
                        ).SetTarget(Unit2, canbe_status=the_status)
                    )

        # Clear temporary look-at visibility after Hex Bolt fully resolves.
        for face in resolving_faces:
            face.card.visible.Clean()
            face.card.visible.Update()

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hex_bolt
        ).SetPlay().SetLabel(),
    ]

