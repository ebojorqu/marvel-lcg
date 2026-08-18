from . import *

class HasToughness(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_toughness: int = 0

        super().__init__(paper)

        self.RegisterAttribute("Toughness", "printed_toughness")
        self.RegisterInfoDict('toughness')

    @override
    def OnAfterCardEnterPlay(self, message: 'Message.AfterCardEnterPlay') -> None:
        from game.effect.rule import Toughness
        from game.operate.faces import Faces
        super().OnAfterCardEnterPlay(message)
        if self.IsToughness() and self.IsInPlay():
            Faces.GiveStatus([self], "Tough", Toughness(self))

    ################################################################################
    #
    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.GainToughness(self.printed_toughness, by_effect)
        return super().OnResetKeywords(by_effect)

    @final
    def IsToughness(self) -> bool:
        return self.toughness > 0

    @final
    @property
    def toughness(self) -> int:
        return self.GetKeyword('Toughness')

    @final
    def GainToughness(self, diff: int, by_effect: 'Effect'):
        self.GainKeyword(diff, 'Toughness', by_effect)

