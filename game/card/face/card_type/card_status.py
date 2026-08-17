from core import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *
from cards.paper import Paper

@final
class StatusCard(FinalType):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.name: CardFace.STATUS
        super().__init__(paper)
        self.symbol_name: str = {
            "Tough": Symbol.tough,
            "Stunned": Symbol.stunned,
            "Confused": Symbol.confused
        }[self.name]

    @override
    def GetAbilities(self) -> List['Ability']:
        from game.card.face.base import Unit2
        from game.operate.faces import Faces

        def remove_this(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
            this = effect.this.CastTo(StatusCard)
            Unused(this)
            message.SetToArea(self.card.world.area_status_cards)

        def send_lost_status(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
            from game.message import Message
            this = effect.this.CastTo(StatusCard)
            if message.from_area.bind_card:
                unit = message.from_area.bind_card.face.CastTo(Unit2)
                discard_message = Message.AfterStatusDiscardFrom(unit, this, message.by_effect)
                discard_message.Send()

        # Build list of abilities
        abilities = [
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Rule,
                "This",
                remove_this
            ).NoOutOfPlayLimit(),
            AbilityFactory.AfterCardDiscard(
                AbilityType.Rule,
                "This",
                send_lost_status
            ).NoOutOfPlayLimit(),
        ]

        # Add Forced Interrupt abilities for status effects per v1.8 rulebook
        # These abilities have TimingPriority.Status (2.a in rulebook) and resolve before regular Forced Interrupts
        status_name = self.name

        if status_name == "Stunned":
            def stunned_interrupt(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
                # Stunned Forced Interrupt: When this character would attack, remove stunned status cards
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                if bound_unit and message.attacker == bound_unit:
                    # Remove all stunned status cards from this character
                    stunned_cards = bound_unit.components.status.deck.FindCards(name="Stunned", card_type=StatusCard)
                    Faces.DiscardAll(stunned_cards, effect)
                    message.SetBeInstead(effect)

            def check_stunned_unit(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
                # Condition: Check if the attacking unit matches this status card's bound unit
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                return bound_unit is not None and message.attacker == bound_unit and bound_unit.IsStunned()

            abilities.append(
                Ability(
                    AbilityType.Status,
                    Message.WhenUnitWouldAttack,
                    [check_stunned_unit],
                    stunned_interrupt,
                    is_local=False
                ).NoOutOfPlayLimit()
            )

        elif status_name == "Confused":
            def confused_interrupt(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
                # Confused Forced Interrupt: When this character would thwart, remove confused status cards
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                if bound_unit and message.thwarter == bound_unit:
                    # Remove all confused status cards from this character
                    confused_cards = bound_unit.components.status.deck.FindCards(name="Confused", card_type=StatusCard)
                    Faces.DiscardAll(confused_cards, effect)
                    message.SetBeInstead(effect)

            def check_confused_unit(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> bool:
                # Condition: Check if the thwarting unit matches this status card's bound unit
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                return bound_unit is not None and message.thwarter == bound_unit and bound_unit.IsConfused()

            abilities.append(
                Ability(
                    AbilityType.Status,
                    Message.WhenUnitWouldThwart,
                    [check_confused_unit],
                    confused_interrupt,
                    is_local=False
                ).NoOutOfPlayLimit()
            )

        elif status_name == "Tough":
            def tough_interrupt(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
                # Tough Forced Interrupt: When this character would take damage, remove a tough status card
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                if bound_unit and message.trigger == bound_unit:
                    # Remove one tough status card from this character
                    tough_cards = bound_unit.components.status.deck.FindCards(name="Tough", card_type=StatusCard, max=1)
                    Faces.DiscardAll(tough_cards, effect)
                    message.SetBeInstead(effect)

            def check_tough_unit(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
                # Condition: Check if the unit taking damage matches this status card's bound unit
                this = effect.this.CastTo(StatusCard)
                bound_unit = this.bind_face
                return bound_unit is not None and message.trigger == bound_unit and bound_unit.IsTough()

            abilities.append(
                Ability(
                    AbilityType.Status,
                    Message.WhenUnitWouldTakeDamage,
                    [check_tough_unit],
                    tough_interrupt,
                    is_local=False
                ).NoOutOfPlayLimit()
            )

        return abilities + super().GetAbilities()

    ################################################################################
    #
    @property
    @override
    def bind_face(self) -> 'Unit2|None':
        unit_card = self.card.area.bind_card
        if unit_card and Unit2.IsType(unit_card.face):
            return unit_card.face
        return None

    @override
    def GetBindFace(self) -> 'Unit2':
        face = super().GetBindFace()
        return face.CastTo(Unit2)

    def IsStatusName(self, name: "CardFace.STATUS") -> bool:
        return super().IsName(name, False, False)

