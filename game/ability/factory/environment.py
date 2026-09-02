from core import *

class AbilityFactoryEnvironment:

    @staticmethod
    def GiveBuffToInPlayWhenApplyThis(
        card_finder: CardTypeMin=None,
        *,
        get_new_value: Callable[['Effect', 'CardFace'], int]|None=None,
        buffs: List[Type['Buff']]|None=None,
        # change_on_event: EventType=OnEvent.NONE,
    ) -> 'Ability':
        from game.ability.factory.environment_helper import GiveKeywordToInPlayWhenApplyThisInternal
        from game.card.face.base import EncounterCard

        change_on_event = OnEvent.Faceup(EncounterCard)

        return GiveKeywordToInPlayWhenApplyThisInternal(
            card_finder,
            get_new_value=get_new_value,
            buffs=buffs,
            # works_for_all_cards=True,
            change_on_event=change_on_event,
        )

    @staticmethod
    def GiveAbilityToInPlayWhenApplyThis(
        card_finder: CardTypeMin=None,
        *,
        get_new_value: Callable[['Effect', 'CardFace'], int]|None=None,
        abilities: List['Ability']|None=None,
        # change_on_event: EventType=OnEvent.NONE,
    ) -> 'Ability':
        from game.ability.factory.environment_helper import GiveKeywordToInPlayWhenApplyThisInternal
        from game.card.face.base import EncounterCard

        change_on_event = OnEvent.Faceup(EncounterCard)

        return GiveKeywordToInPlayWhenApplyThisInternal(
            card_finder,
            get_new_value=get_new_value,
            abilities=abilities,
            # works_for_all_cards=True,
            change_on_event=change_on_event,
        )

    # @staticmethod
    # def GiveInciteToEncounterCardWhenApplyThis(
    #     finder: CardTypeMin=None,
    #     *,
    #     incite: int,
    #     not_include_this: bool=False,
    #     trigger_when_reveal: bool=False,
    # ) -> 'Ability':

    #     from game.ability.factory.environment_helper import GiveKeywordToInPlayWhenApplyThisInternal
    #     return GiveKeywordToInPlayWhenApplyThisInternal(
    #         finder,
    #         incite=incite,
    #         not_include_this=not_include_this,
    #         trigger_when_reveal=trigger_when_reveal,
    #         change_on_event=OnEvent.Reveal(finder)
    #     )

    @staticmethod
    def GiveKeywordToInPlayWhenApplyThis(
        card_finder: CardTypeMin|Literal["You", "EnemyLeader"]=None, # give to which card
        *,
        control_by: Literal["You", "EngagedPlayer"]|None=None,
        get_new_value: Callable[['Effect', 'CardFace'], int|List[str]]|None=None,
        condition: Callable[['Effect'], bool]|None=None,
        if_each_of_your_characters_has_trait: "CardFace.TRAITS|None"=None,
        if_each_of_your_allies_has_trait: "CardFace.TRAITS|None"=None,
        works_in_the_victory_display: bool=False, # 40006
        expert_mode_only: Literal[True]|None=None,
        not_include_this: bool=False,
        #
        ally_limit: int|None=None,
        flag: 'PlayerFlag.FLAG|None'=None,
        #
        trait: List["CardFace.TRAITS"]|"CardFace.TRAITS|None"|Literal[1]=None,
        teamwork: List["CardFace.TRAITS"]|"CardFace.TRAITS|None"|Literal[1]=None,
        attack: int|None=None,
        defense: int|None=None,
        thwart: int|None=None,
        scheme: int|None=None,
        retaliate: int|None=None,
        hand_size: int|None=None,
        stalwart: int|None=None,
        health: int|None=None,
        recover: int|None=None,
        guard: int|None=None,
        steady: int|None=None,
        treat_as_blank: bool|None=None,
        quickstrike :int|None=None,
        attack_consequential_damage: int|None=None,
        thwart_consequential_damage: int|None=None,
        patrol: int|None=None,
        surge: int|None=None,
        acceleration_icon: int|None=None,
        hazard: int|None=None,
        toughness: int|None=None,
        peril: int|None=None,
        incite: int|None=None,
        temporary: int|None=None,
        permanent: int|None=None,
        villainous:  int|None=None,
        target_threat: int|None=None,
        additional_cost_for_basic_attack: 'CostFunc.Base|None'=None,
        additional_cost_for_basic_thwart: 'CostFunc.Base|None'=None,
        additional_cost_for_basic_defend: 'CostFunc.Base|None'=None,
        apply: Callable[['Effect', 'CardFace', int], None]|None=None,
        base_sch: int|None=None,
        base_atk: int|None=None,
        base_health: int|None=None,
        change_on_event: EventType=OnEvent.NONE,
        # apply: Callable[['Effect','CardFace', int], None]|None=None,
        ) -> List['Ability']:
        from game.ability.factory.environment_helper import GiveKeywordToInPlayWhenApplyThisInternal
        from game.card.card_finder import CardFinder

        if if_each_of_your_allies_has_trait:
            assert change_on_event == OnEvent.NONE
            change_on_event = OnEvent.Trait("YourAlly")
            change_on_event = Condition.AddEvent(change_on_event, OnEvent.PlayAreaCard("YourAlly"))
            # assert isinstance(change_on_event, OnEvent.Trait)

        if change_on_event == OnEvent.NONE and isinstance(card_finder, CardFinder):
            if card_finder.trait  is not None:
                # assert isinstance(change_on_event, OnEvent.Trait)
                assert len(card_finder.params) == 2
                change_on_event = OnEvent.Trait(card_finder.card_type)

        if flag:
            assert card_finder == "You"

        if card_finder == "You":
            card_finder = "YourIdentity"
        if card_finder == "EnemyLeader":
            card_finder = Leader

        abilities: List['Ability'] = []

        if trait  is not None or \
            teamwork  is not None or \
            attack  is not None or \
            defense  is not None or \
            thwart  is not None or \
            scheme  is not None or \
            retaliate  is not None or \
            hand_size  is not None or \
            stalwart  is not None or \
            health  is not None or \
            recover  is not None or \
            guard  is not None or \
            steady  is not None or \
            treat_as_blank  is not None or \
            quickstrike  is not None or \
            attack_consequential_damage  is not None or \
            thwart_consequential_damage  is not None or \
            patrol  is not None or \
            surge  is not None or \
            acceleration_icon  is not None or \
            hazard  is not None or \
            toughness  is not None or \
            peril  is not None or \
            incite  is not None or \
            temporary  is not None or \
            permanent  is not None or \
            villainous  is not None or \
            target_threat  is not None or \
            additional_cost_for_basic_attack  is not None or \
            additional_cost_for_basic_thwart  is not None or \
            additional_cost_for_basic_defend  is not None or \
            base_sch  is not None or \
            base_atk  is not None or \
            base_health  is not None or \
            apply  is not None:

            abilities.append(GiveKeywordToInPlayWhenApplyThisInternal(
                card_finder=card_finder,
                control_by=control_by,
                get_new_value=get_new_value,
                condition=condition,
                if_each_of_your_characters_has_trait=if_each_of_your_characters_has_trait,
                if_each_of_your_allies_has_trait=if_each_of_your_allies_has_trait,
                works_in_the_victory_display=works_in_the_victory_display,
                expert_mode_only=expert_mode_only,
                ignore_flip=False,
                not_include_this=not_include_this,
                #,
                trait=trait,
                teamwork=teamwork,
                attack=attack,
                defense=defense,
                thwart=thwart,
                scheme=scheme,
                retaliate=retaliate,
                hand_size=hand_size,
                stalwart=stalwart,
                health=health,
                recover=recover,
                guard=guard,
                steady=steady,
                treat_as_blank=treat_as_blank,
                quickstrike=quickstrike,
                attack_consequential_damage=attack_consequential_damage,
                thwart_consequential_damage=thwart_consequential_damage,
                patrol=patrol,
                surge=surge,
                acceleration_icon=acceleration_icon,
                hazard=hazard,
                toughness=toughness,
                peril=peril,
                incite=incite,
                temporary=temporary,
                permanent=permanent,
                villainous=villainous,
                target_threat=target_threat,
                additional_cost_for_basic_attack=additional_cost_for_basic_attack,
                additional_cost_for_basic_thwart=additional_cost_for_basic_thwart,
                additional_cost_for_basic_defend=additional_cost_for_basic_defend,
                base_sch=base_sch,
                base_atk=base_atk,
                base_health=base_health,
                apply=apply,
                change_on_event=change_on_event
            ))

        if ally_limit  is not None or flag  is not None:
            abilities.append(GiveKeywordToInPlayWhenApplyThisInternal(
                card_finder=card_finder,
                control_by=control_by,
                get_new_value=get_new_value,
                condition=condition,
                if_each_of_your_characters_has_trait=if_each_of_your_characters_has_trait,
                if_each_of_your_allies_has_trait=if_each_of_your_allies_has_trait,
                works_in_the_victory_display=works_in_the_victory_display,
                expert_mode_only=expert_mode_only,
                ignore_flip=True,
                not_include_this=not_include_this,
                #
                ally_limit=ally_limit,
                flag=flag,
                change_on_event=change_on_event
            ))

        if incite:
            abilities.append(
                GiveKeywordToInPlayWhenApplyThisInternal(
                    card_finder,
                    get_new_value=get_new_value,
                    incite=incite,
                    not_include_this=not_include_this,
                    incite_only=True,
                    change_on_event=OnEvent.Reveal(card_finder)
                )
            )

        return abilities

