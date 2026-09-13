from . import *

# * Wonder Man

def GetAbilities() -> Sequence['Ability']:

    def get_ionic_tucked_count(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)

        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
        )
        if not ionic_physiology:
            return 0
        return ionic_physiology.GetPlacedCardArea().GetSize()

    def power_recycling(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        ionic_physiology = Worlds.FindCardOnField(
            effect,
            name="Ionic Physiology",
            card_type=Upgrade,
        )
        if not ionic_physiology:
            return

        tucked_cards = ionic_physiology.GetPlacedCardArea().GetAll()
        if tucked_cards:
            Faces.DiscardAll(tucked_cards, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            get_ionic_tucked_count,
            attack=1,
            change_on_event=OnEvent.TuckUnder("Identity"),
        ).SetName("Power Recycling"),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            power_recycling,
            is_basic_attack=True,
        ),
    ]