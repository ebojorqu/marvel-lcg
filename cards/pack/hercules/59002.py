from . import *

# Defeat the Hydra

def GetAbilities() -> Sequence['Ability']:

    def defeat_the_hydra_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        minion = Search.EncounterCard(
            effect,
            effect.GetInitiator(),
            include_discard_pile=True,
            include_set_aside=True,
            card_type=Minion,
            non_trait="ELITE",
            check_effect_fn=lambda check_effect, face: face.printed_health >= 6,
        )
        if minion:
            minion.Reveal(effect.GetInitiator(), effect)
            minion.SetHealth(minion.starting_health, effect)
            this.AttachTo2(minion, effect)

    def only_hercules_can_damage(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        if this.GetAttached() != message.target:
            return False
        if not message.would_attack_unit_message:
            return True
        attacker = message.would_attack_unit_message.attacker
        if not attacker:
            return True
        owner_name = this.GetOwnerPlayer().GetIdentity().name
        return attacker.GetControlByPlayer().GetIdentity().name != owner_name

    def prevent_damage(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.CancelDamage(effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "AttachedCharacter",
            health=6,
            trait="ELITE",
        ),
        AbilityFactory.WhenCardRevealed(
            AbilityType.WhenRevealed,
            "This",
            defeat_the_hydra_revealed,
        ),
        AbilityFactory.WhenFaceWouldDealDamage(
            AbilityType.NonKeyword,
            "AnyCard",
            prevent_damage,
            conditions=[only_hercules_can_damage],
        ).NoOutOfPlayLimit(),
    ]
