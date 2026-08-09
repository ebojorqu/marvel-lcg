from . import *

# Embody Pathos

def GetAbilities() -> Sequence['Ability']:

    def embody_pathos_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        scheme = Search.EncounterCard(
            effect,
            effect.GetInitiator(),
            include_discard_pile=True,
            include_set_aside=True,
            card_type=SchemeSide2,
            check_effect_fn=lambda check_effect, face: not face.IsInPlay(),
        )
        if scheme:
            scheme.Reveal(effect.GetInitiator(), effect)
            this.AttachTo2(scheme, effect)
            scheme.PlaceThreat(6, effect)

    def only_hercules_can_remove_threat(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> bool:
        this = effect.this.CastTo(Attachment)
        if this.GetAttached() not in message.schemes:
            return False
        owner_name = this.GetOwnerPlayer().GetIdentity().name
        return message.attacker.GetControlByPlayer().GetIdentity().name != owner_name

    def cancel_thwart(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        message.GainValue(-message.will_remove_threat, effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            embody_pathos_revealed,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Scheme2,
            assault=1,
        ),
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            "AnyCard",
            cancel_thwart,
            thwarted_scheme="AnyCard",
            conditions=[only_hercules_can_remove_threat],
        ).NoOutOfPlayLimit(),
    ]
