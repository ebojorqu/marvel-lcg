from . import *

# Ares's Axe

def GetAbilities() -> Sequence['Ability']:

    def attach(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Attachment)
        ares = Worlds.FindCardOnField(effect, name="Ares", card_type=Minion)
        if ares:
            this.AttachTo2(ares, effect)
            return

        villain = Worlds.GetMainVillain(effect)
        this.AttachTo2(villain, effect)

    def discard_if_no_friendly_took_damage(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        attached = effect.this.bind_face
        if attached != message.attacker:
            return

        against = message.GetAgainstPlayer()
        if against is None:
            return

        took_friendly_damage = any(x.GetControlByPlayer() == against for x in message.damaged_targets)
        if not took_friendly_damage:
            Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.NonKeyword,
            "This",
            attach,
        ),
        *AbilityFactory.GiveKeywordToAttached("AttachedEnemy", attack=2),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            Enemy,
            discard_if_no_friendly_took_damage,
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).NoOutOfPlayLimit(),
    ]
