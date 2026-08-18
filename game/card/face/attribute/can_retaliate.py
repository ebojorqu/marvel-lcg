from . import *

class HasRetaliate(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_retaliate = 0

        super().__init__(paper)

        self.RegisterAttribute("Retaliate", "printed_retaliate")
        self.RegisterInfoDict('retaliate')

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.GainRetaliate(self.printed_retaliate, by_effect)
        return super().OnResetKeywords(by_effect)

    ################################################################################
    #
    @final
    def GainRetaliate(self, diff: int, by_effect: 'Effect'):
        self.GainKeyword(diff, 'Retaliate', by_effect)

    @final
    @property
    def retaliate(self) -> int:
        return self.GetKeyword('Retaliate')

class CanRetaliate(HasRetaliate):

    @override
    def GetAbilities(self) -> List['Ability']:
        from game.ability import AbilityType
        from game.ability.factory import AbilityFactory

        abilities = [
            AbilityFactory.AfterUnitAttackUnitInternal(
                AbilityType.ForcedResponse,
                None,
                None,
                lambda effect, message:
                    effect.this.ResolveRetaliate(message.would_atk_unit_message),
                conditions=[
                    lambda effect, message:
                        message.attacked == effect.this,
                ],
            )
        ]
        return abilities + super().GetAbilities()

    @final
    def ResolveRetaliate(self, atk_message: 'Message.WhenUnitWouldAttackUnit'):
        from game.effect.rule import Retaliate

        if self.retaliate > 0:
            attacker = atk_message.attacker
            if attacker and not attacker.IsDefeated():
                if not atk_message.IsRanged() and \
                    not self.IsDefeated() and \
                    not atk_message.IsIgnoreRetaliate():
                    return attacker.TakeDamage(self, self.retaliate, Retaliate(self))
                else:
                    ignore_message = Message.AfterIgnoreKeywordOnCard(attacker, [self], "Retaliate")
                    ignore_message.Send()
                    return None

