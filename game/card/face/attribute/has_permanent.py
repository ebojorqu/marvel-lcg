from . import *

class HasPermanent(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_permanent = False

        super().__init__(paper)

        self.RegisterAttribute("Permanent", "printed_permanent", bool)
        self.RegisterInfoDict('permanent')

    @override
    def GetAbilities(self) -> List['Ability']:
        from game.ability import AbilityType
        from game.message import Message

        def check_foreign_blank(effect: 'Effect', message: 'Message.WhenCardWouldTreatAsIfBlank') -> bool:
            return self.permanent and \
                message.trigger == self and \
                message.by_effect.this.paper.set_name != self.paper.set_name

        abilities = [
            Ability(
                AbilityType.NonKeyword,
                Message.WhenCardWouldTreatAsIfBlank,
                [check_foreign_blank],
                lambda effect, message: message.SetBeInstead(effect),
            )
        ]
        return abilities + super().GetAbilities()

    @override
    def OnWouldDefeated(self, killer: 'CardFace|None', by_effect: 'Effect', being_message: 'Message.WhenSchemeBeingThwart|Message.WhenUnitBeingAttack|None') -> 'Message.WhenSchemeWouldBeDefeated|Message.WhenUnitWouldBeDefeated|None':
        if self.permanent and by_effect.this.paper.set_name != self.paper.set_name:
            return None
        return super().OnWouldDefeated(killer, by_effect, being_message)

    ################################################################################
    #
    @override
    def OnWhenCardLeavePlay(self, message: 'Message.WhenCardLeavePlay') -> bool:
        from game.player import Player
        if self.permanent:
            # Hack
            by_effect = message.by_effect
            if self.paper.set_name in ["Flight", "Super Strength", "Telepathy"]:
                if by_effect.this.paper.card_id == "40139a":
                    pass
            elif self.paper.set_name == "Weather":
                if by_effect.this.paper.set_name == "Storm":
                    pass
            elif self.name == "Power Stone":
                controller = self.GetBindFace().GetControlBy()
                if Player.IsType(controller) and controller.is_eliminated:
                    from game.operate.worlds import Worlds
                    villain = Worlds.FindVillain(by_effect)
                    if villain:
                        self.CastTo(CanAttach).AttachTo2(villain, by_effect)
                        return False
            elif self.name == "Milano":
                if by_effect.this.name == "The Missing Milano":
                    pass
            elif self.paper.set_name != by_effect.this.paper.set_name:
                return False
        return super().OnWhenCardLeavePlay(message)

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.GainPermanent(self.printed_permanent, by_effect)
        return super().OnResetKeywords(by_effect)

    @final
    def GainPermanent(self, diff: int, by_effect: 'Effect'):
        self.GainKeyword(diff, 'Permanent', by_effect)

    @final
    @property
    def permanent(self) -> bool:
        return self.GetKeyword('Permanent') > 0

