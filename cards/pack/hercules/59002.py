from . import *

# Defeat the Hydra

def GetAbilities() -> Sequence['Ability']:

    def defeat_the_hydra_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        player = message.GetToPlayer()

        minion = Search.EncounterCard(
            effect,
            player,
            include_discard_pile=True,
            include_set_aside=True,
            card_type=Minion,
            non_trait="ELITE",
            check_effect_fn=lambda check_effect, face: face.printed_health >= 6,
        )
        if minion:
            minion.Reveal(player, effect)
            minion.SetHealth(minion.starting_health, effect)
            this.AttachTo2(minion, effect)

    def only_hercules_can_damage(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        if not message.would_attack_unit_message:
            return True
        attacker = message.would_attack_unit_message.attacker
        if not attacker:
            return True
        return not attacker.IsName("Hercules")

    def prevent_damage(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.PreventDamage("All", effect)

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
            None,
            prevent_damage,
            who_take_damage="AttachedCharacter",
            conditions=[only_hercules_can_damage],
        ).NoOutOfPlayLimit(),
    ]
