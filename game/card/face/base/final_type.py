from game.card.face.card_face import CardFace

class FinalType(CardFace):
    is_final = True

    @property
    def type_name(self) -> str:
        return self.__class__.__name__

