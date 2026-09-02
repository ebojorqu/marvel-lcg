import sys
from typing import Literal
import unittest
from build import Build

class TestMain(unittest.TestCase):

    def RunCases(self, var_name: Literal["min_test_folder", "profile_folder", "all"],
                *,
                release: bool=True,
                profile: bool=False):
        if release:
            Build.release = True
        else:
            Build.release = False

        # import types
        # debug_module = types.ModuleType('core.utility.debug')
        # sys.modules['core.utility.debug'] = debug_module
        # with open('./core/utility/debug.py') as f:
        #     exec(f.read(), debug_module.__dict__)
        # IsVSDebug = debug_module.Debug.IsVSDebug
        from core.utility.debug import Debug
        IsVSDebug = Debug.IsVSDebug

        sys.argv.append("-config_files")
        sys.argv.append("launch-debug.json")

        sys.argv.append('-test')

        sys.argv.append('-test_result_file')
        sys.argv.append(f"test_{var_name}{'_release' if release else '_debug'}{'_profile' if profile else ''}{'_trace' if IsVSDebug() else '_notrace'}.log")

        sys.argv.append('-enable_profile_category')
        sys.argv.append('Test')

        from engine import Engine
        from unit_test.entry import TestEntry
        from unit_test.runner import TestRunner
        from engine.config import ConfigVariables

        ConfigVariables.Folder('min_test_folder', "./replays/min_test/")
        ConfigVariables.Folder('profile_folder', "./replays/profiles/")

        if var_name == "all":
            folder = None
        else:
            var = ConfigVariables.Find(var_name)
            assert var and isinstance(var.value, str)
            folder = var.value

        if Engine.Initialize():
            Engine.in_unit_test = True
            TestRunner.Execute(TestEntry.Test, folder, profile)
            Engine.Shutdown()

    def test_rapid_response_hero_defend_player_resolution(self):
        from types import SimpleNamespace
        import game.player as player_module
        import game.card.face.card_type as card_type_module
        from game.ability.condition import Condition

        class FakePlayer:
            def __init__(self, identity):
                self._identity = identity
            def GetIdentity(self):
                return self._identity
            def GetRoleCharacter(self):
                return self._identity
            def IsScenario(self):
                return False
            @staticmethod
            def IsType(obj):
                return isinstance(obj, FakePlayer)

        class FakeIdentity:
            def __init__(self, controller):
                self._controller = controller
            @staticmethod
            def IsType(obj):
                return isinstance(obj, FakeIdentity)
            def GetControlBy(self):
                return self._controller

        class FakeFace:
            def __init__(self, control_by):
                self.card = SimpleNamespace(area=SimpleNamespace(flags=SimpleNamespace(is_obligations_area=False)))
                self._control_by = control_by
            def GetControlByOrOwner(self):
                return self._control_by
            def GetControlBy(self):
                return self._control_by

        class FakeAlly(FakeFace):
            @staticmethod
            def IsType(obj):
                return isinstance(obj, FakeAlly)

        class FakeUpgrade(FakeIdentity):
            def __init__(self, bind_face):
                super().__init__(bind_face._control_by)
                self.bind_face = bind_face
            def GetBindFace(self):
                return self.bind_face

        old_player = player_module.Player
        old_identity = card_type_module.Identity
        old_upgrade = card_type_module.Upgrade
        old_ally = card_type_module.Ally
        old_event = card_type_module.Event
        try:
            player_module.Player = FakePlayer
            card_type_module.Identity = FakeIdentity
            card_type_module.Upgrade = FakeUpgrade
            card_type_module.Ally = FakeAlly
            card_type_module.Event = type('FakeEvent', (), {})

            defending_player = FakePlayer(FakeIdentity(None))
            identity = FakeIdentity(defending_player)
            attack_target_player = FakePlayer(identity)
            effect = SimpleNamespace(
                this=FakeFace(defending_player),
                initiator=attack_target_player,
                context=SimpleNamespace(ask_player=defending_player),
            )

            self.assertTrue(Condition.ThisIsYou(effect, identity))

            ally_face = FakeAlly(attack_target_player)
            self.assertTrue(Condition.CheckWhichCard("YouControlAlly", [ally_face], effect))
        finally:
            player_module.Player = old_player
            card_type_module.Identity = old_identity
            card_type_module.Upgrade = old_upgrade
            card_type_module.Ally = old_ally
            card_type_module.Event = old_event

    def test_card_finder_and_conflicting_filters_are_handled_without_asserting(self):
        from game.card.card_finder.finder import CardFinder
        from game.card.card_finder.finder import CardFinder2

        finder = CardFinder(name="Ultron Drones", card_type=__import__('game.card.face.card_type', fromlist=['Environment']).Environment)
        other = CardFinder(name="Ultron Drones", card_type=__import__('game.card.face.card_type', fromlist=['Minion']).Minion)

        merged = finder & other
        self.assertTrue(hasattr(merged, 'always_false'))
        self.assertTrue(merged.always_false)
        self.assertTrue(bool(merged))

        ultron_finder = CardFinder2("DRONE", __import__('game.card.face.card_type', fromlist=['Minion']).Minion)
        self.assertEqual(len(ultron_finder.params), 2)

    def test_setup_cards_put_into_play_honors_set_aside_source_without_prompting(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from game.operate.setup_cards import SetupCards
        from game.operate.worlds import Worlds
        from game.operate.search_internal import SearchInternal

        class FakeFace:
            def __init__(self):
                self.card = SimpleNamespace(face=self)
            def PutIntoPlay(self, *args, **kwargs):
                return True

        fake_face = FakeFace()
        fake_effect = SimpleNamespace(world=SimpleNamespace(GetFirstPlayer=lambda: object()))

        with patch.object(Worlds, 'GetSetAsideAreaCards', return_value=[fake_face]) as get_set_aside, \
             patch.object(SearchInternal, 'FindCards', side_effect=AssertionError('generic search should not be used')):
            result = SetupCards.PutIntoPlay(
                fake_effect,
                name='Ultron Drones',
                card_type=__import__('game.card.face.card_type', fromlist=['Environment']).Environment,
                from_where=['SetAside'],
            )

        self.assertIs(result, fake_face)
        get_set_aside.assert_called_once()

    def test_final_card_type_matching_allows_leadership_event_target_selection(self):
        from cards.database import CardsDB
        from game.card.card_finder import CardFinder
        from game.card.face.card_type import Event

        CardsDB.Initialize()
        paper = CardsDB.FindCardPaper('01069')
        face = Event(paper)
        face.Initialize(0)

        self.assertTrue(face.IsTypeOld(Event))
        self.assertTrue(CardFinder(card_type=Event).Check(face, None))
        self.assertTrue(CardFinder(card_type=Event, card_class='Leadership').Check(face, None))

    def test_message_to_player_accepts_runtime_player_instance_even_if_alias_is_stale(self):
        import game.player as player_module
        from game.message.message_type import TriggerNonePlayerMessage
        from game.player.player import Player

        class FakeController:
            def __init__(self):
                self.manager = None

        class FakeScene:
            def __init__(self):
                self.players = [type('PlayerInfo', (), {'name': 'Alpha', 'hero': ['31002a'], 'hero_deck': [], 'obligations': [], 'nemesis_set': [], 'player_deck': []})()]
                self.campaign = type('Campaign', (), {'campaign_log': {}})()

        old_player_alias = player_module.Player
        stale_alias = type('Player', (), {})
        try:
            player_module.Player = stale_alias
            world = __import__('game.world.world', fromlist=['World']).World
            # Build the minimal runtime object needed by the message assertion.
            scene = FakeScene()
            world_obj = world(scene, [FakeController()])
            runtime_player = Player('Alpha', world_obj.controller_manager, 0, world_obj)
            message = TriggerNonePlayerMessage(runtime_player, world=world_obj)
            self.assertIs(message.GetToPlayer(), runtime_player)
            self.assertTrue(message.IsToPlayer())
        finally:
            player_module.Player = old_player_alias

    def test_after_unit_attack_unit_get_to_player_ignores_card_specific_assertion(self):
        from types import SimpleNamespace

        message = object.__new__(__import__('game.message.sender.sender_damage', fromlist=['Message']).Message.AfterUnitAttackUnit)
        message.attacked_you = object()
        message.by_effect = SimpleNamespace(
            this=SimpleNamespace(paper=SimpleNamespace(card_id='99999')),
            world=SimpleNamespace(GetCurrentPlayer=lambda: 'fallback_player'))

        self.assertEqual(message.GetToPlayer(), 'fallback_player')

    def test_canbe_confused_uses_runtime_buff_symbol(self):
        from game.card.face.attribute.can_status import CanStatus

        status = object.__new__(CanStatus)
        status.IsInPlay = lambda: True
        status.IsStalwart = lambda: False
        status.IsConfused = lambda: False
        status.GetBuff = lambda _buff: False

        self.assertTrue(status.CanbeConfused())

    def test_status_card_uses_runtime_symbol_namespace(self):
        from cards.paper import Paper
        from game.card.face.card_type.card_status import StatusCard

        paper = Paper('status-1', '', 'Status', False, 'Confused', '', {}, [], '', '', '')
        card = StatusCard(paper)

        self.assertEqual(card.symbol_name, __import__('game.render.symbol', fromlist=['Symbol']).Symbol.confused)

    def test_zero_defense_is_hidden_for_cards_without_defense_value(self):
        from types import SimpleNamespace
        from game.card.face.attribute.can_defense import HasDefense

        face = object.__new__(HasDefense)
        face.info_dict = ['defense']
        face.printed_defense = 0
        face.card = SimpleNamespace(area=SimpleNamespace(GetOwner=lambda: SimpleNamespace(IsPlayer=lambda: False)))
        face.GetKeyword = lambda _key: 0
        face.GetBuff = lambda _buff: False
        face.consider_as = ""

        self.assertNotIn('defense', face.GetInfoDict())

    def test_discard_until_stops_at_first_matching_ally(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from game.deck.deck import Deck2

        class FakeFace:
            def __init__(self, name, deck, *, is_ally=False):
                self.name = name
                self.deck = deck
                self.is_ally = is_ally
                self.discarded = False
            def IsName(self, name):
                return self.name == name
            def IsSubName(self, name):
                return False
            def HasTrait(self, *traits):
                return False
            def IsTypeOld(self, card_type):
                return self.is_ally and issubclass(card_type, FakeAlly)
            def DiscardInternal(self, by_effect):
                self.discarded = True
                self.deck.cards = [c for c in self.deck.cards if c is not self]

        class FakeAlly(FakeFace):
            def __init__(self, name, deck):
                super().__init__(name, deck, is_ally=True)

        deck = object.__new__(Deck2)
        deck.flags = SimpleNamespace(is_deck=True, is_discards=False, is_player_deck=False)
        deck.cards = []
        energy = FakeFace('Energy', deck)
        ally = FakeAlly('Professor X', deck)
        later = FakeFace('Later', deck)
        deck.cards = [later, ally, energy]
        deck.Get = lambda from_top=False: list(reversed(deck.cards)) if from_top else list(deck.cards)
        deck.GetSize = lambda: len(deck.cards)

        with patch('game.message.Message.AfterCardsMoved') as after_cards_moved:
            after_cards_moved.return_value.Send = lambda: None
            found, other_faces = deck.DiscardUntil(object(), name=None, trait=None, card_type=FakeAlly)

        self.assertIs(found, ally)
        self.assertEqual([face.name for face in other_faces], ['Energy'])
        self.assertTrue(ally.discarded)
        self.assertFalse(later.discarded)

    def test_discard_until_returns_last_matching_ally(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from game.deck.deck import Deck2

        class FakeFace:
            def __init__(self, name, deck, *, is_ally=False):
                self.name = name
                self.deck = deck
                self.is_ally = is_ally
                self.discarded = False
            def IsName(self, name):
                return self.name == name
            def IsSubName(self, name):
                return False
            def HasTrait(self, *traits):
                return False
            def IsTypeOld(self, card_type):
                return self.is_ally and issubclass(card_type, FakeAlly)
            def DiscardInternal(self, by_effect):
                self.discarded = True
                self.deck.cards = [c for c in self.deck.cards if c is not self]

        class FakeAlly(FakeFace):
            def __init__(self, name, deck):
                super().__init__(name, deck, is_ally=True)

        deck = object.__new__(Deck2)
        deck.flags = SimpleNamespace(is_deck=True, is_discards=False, is_player_deck=False)
        deck.cards = []
        ally = FakeAlly('Professor X', deck)
        deck.cards = [ally]
        deck.Get = lambda from_top=False: list(deck.cards)
        deck.GetSize = lambda: len(deck.cards)

        with patch('game.message.Message.AfterCardsMoved') as after_cards_moved:
            after_cards_moved.return_value.Send = lambda: None
            found, other_faces = deck.DiscardUntil(object(), name=None, trait=None, card_type=FakeAlly)

        self.assertIs(found, ally)
        self.assertEqual(other_faces, [])
        self.assertTrue(ally.discarded)

    def test_discard_until_checks_top_card_before_discarding_it(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from game.deck.deck import Deck2

        class FakeFace:
            def __init__(self, name, deck, *, is_ally=False):
                self.name = name
                self.deck = deck
                self.is_ally = is_ally
                self.discarded = False
            def IsName(self, name):
                return self.name == name
            def IsSubName(self, name):
                return False
            def HasTrait(self, *traits):
                return False
            def IsTypeOld(self, card_type):
                return self.is_ally and issubclass(card_type, FakeAlly)
            def DiscardInternal(self, by_effect):
                self.discarded = True
                self.deck.cards = [c for c in self.deck.cards if c is not self]

        class FakeAlly(FakeFace):
            def __init__(self, name, deck):
                super().__init__(name, deck, is_ally=True)

        deck = object.__new__(Deck2)
        deck.flags = SimpleNamespace(is_deck=True, is_discards=False, is_player_deck=False)
        deck.cards = []
        other = FakeFace('Energy', deck)
        ally = FakeAlly('Professor X', deck)
        later = FakeFace('Later', deck)
        deck.cards = [later, ally, other]
        deck.Get = lambda from_top=False: list(reversed(deck.cards)) if from_top else list(deck.cards)
        deck.GetSize = lambda: len(deck.cards)

        with patch('game.message.Message.AfterCardsMoved') as after_cards_moved:
            after_cards_moved.return_value.Send = lambda: None
            found, other_faces = deck.DiscardUntil(object(), name=None, trait=None, card_type=FakeAlly)

        self.assertIs(found, ally)
        self.assertEqual([face.name for face in other_faces], ['Energy'])
        self.assertTrue(ally.discarded)
        self.assertTrue(other.discarded)
        self.assertFalse(later.discarded)

    def test_undo_keeps_only_the_last_valid_history(self):
        from types import SimpleNamespace

        class DummySkip:
            def __init__(self):
                self.skip_to = 0
            def SetSkipTo(self, value):
                self.skip_to = value

        replay = SimpleNamespace(history_inputs=[1, 2, 3, 4], current_step_id=4, replay_step_id=4, is_updated=False, calculated_crc=[])
        replay.Clear = lambda: None
        replay.SetReplayInputs = lambda inputs: setattr(replay, 'replay_inputs', list(inputs))
        replay.Clean = lambda: None
        game = SimpleNamespace()
        game.controller_manager = SimpleNamespace(
            replay=replay,
            skip=DummySkip(),
        )
        game.scene = SimpleNamespace(inputs=[1, 2, 3, 4])
        game.state = SimpleNamespace(SetStartState=lambda _state: None)
        game.ApplyHistoryInput = lambda: None

        session = __import__('game.game_run.game_session', fromlist=['GameSession']).GameSession(game)
        session.world = SimpleNamespace(game_over=SimpleNamespace(SetUndo=lambda: None))
        session.ExitWait = lambda: None

        session.Undo(1)

        self.assertEqual(game.controller_manager.replay.history_inputs, [1, 2, 3])
        self.assertEqual(game.controller_manager.replay.current_step_id, 3)
        self.assertEqual(game.controller_manager.replay.replay_step_id, 3)
        self.assertEqual(game.scene.inputs, [1, 2, 3])
        self.assertEqual(game.controller_manager.skip.skip_to, 3)

    def test_set_scene_resets_replay_state(self):
        from types import SimpleNamespace

        replay = SimpleNamespace(
            history_inputs=[1, 2, 3],
            replay_inputs=[1, 2, 3],
            current_step_id=3,
            replay_step_id=3,
            is_updated=True,
            calculated_crc=['x'],
        )
        replay.Clean = lambda: setattr(replay, 'history_inputs', []) or setattr(replay, 'current_step_id', 0) or setattr(replay, 'replay_step_id', 0) or setattr(replay, 'is_updated', False) or setattr(replay, 'calculated_crc', [])
        replay.SetReplayInputs = lambda inputs: setattr(replay, 'replay_inputs', list(inputs))
        game = SimpleNamespace(
            controller_manager=SimpleNamespace(replay=replay),
            state=SimpleNamespace(SetStartState=lambda _state: None),
        )
        session = __import__('game.game_run.game_session', fromlist=['GameSession']).GameSession(game)
        scene = SimpleNamespace(version='1.0', inputs=[9, 10])

        session.SetScene(scene, 'New')

        self.assertEqual(replay.current_step_id, 0)
        self.assertEqual(replay.replay_step_id, 0)
        self.assertEqual(replay.history_inputs, [])
        self.assertEqual(replay.replay_inputs, [9, 10])

    def test_present_force_no_wait_clears_skip_flag(self):
        from types import SimpleNamespace

        skip = SimpleNamespace(is_skipping=True, SetIsSkipping=lambda skip_value: setattr(skip, 'is_skipping', skip_value) or True)
        world = SimpleNamespace(controller_manager=SimpleNamespace(skip=skip))
        render = SimpleNamespace()
        render.PresentInternal = lambda *args, **kwargs: None
        world_render = __import__('game.world.world_render', fromlist=['WorldRender']).WorldRender(world)
        world_render.PresentInternal = lambda *args, **kwargs: None
        world_render.PresentForceNoWait()
        self.assertFalse(skip.is_skipping)

    def test_shuffle_with_discard_pile_forces_render_after_reset(self):
        from types import SimpleNamespace
        from unittest.mock import patch

        from game.deck.deck import Deck2

        class FakeDeck:
            def __init__(self, cards):
                self.cards = list(cards)
                self.flags = SimpleNamespace(is_deck=False, is_discards=False, is_player_deck=False)
            def Get(self, from_top=False):
                return list(self.cards)
            def GetSize(self):
                return len(self.cards)
            def GetFalse(self):
                return list(self.cards)
            def GetAll(self, from_top=False, include_removed=True):
                return list(self.cards)
            def Clear(self):
                self.cards.clear()
            def __bool__(self):
                return True

        deck = object.__new__(Deck2)
        discard = FakeDeck(['a', 'b'])
        deck.bind_discard_pile = discard
        deck.shuffle_with_discard_count = 0
        deck.flags = SimpleNamespace(is_deck=True, is_discards=False, is_player_deck=False)
        deck.process_after_shuffle = lambda _deck, _effect: None
        deck.world = SimpleNamespace(render=SimpleNamespace(PresentForceNoWait=lambda: None))
        deck.ShuffleInternal = lambda by_effect, only_for_most_top=None: None

        with patch.object(deck.world.render, 'PresentForceNoWait', wraps=deck.world.render.PresentForceNoWait) as render_mock:
            with patch('game.operate.faces.Faces.MoveAllTo', return_value=['a', 'b']):
                with patch('game.message.Message.AfterDeckReset') as after_reset:
                    after_reset.return_value.Send = lambda: None
                    deck.ShuffleWithDiscardPile(False, object())

        render_mock.assert_called_once_with()

    def test_starting_max_one_per_deck(self):
        from game.card.face.attribute.has_starting import HasStarting

        class FakeDeck:
            def __init__(self, owner):
                self.owner = owner
                self.cards = []
            def GetAll(self):
                return self.cards

        class FakePlayer:
            def __init__(self):
                self.player_deck = FakeDeck(self)

        player = FakePlayer()
        start1 = object.__new__(HasStarting)
        start1.printed_starting = 1
        start1.GetControlByOrOwner = lambda: player
        existing = object.__new__(HasStarting)
        existing.printed_starting = 1
        player.player_deck.cards = [existing, start1]

        self.assertFalse(start1.CanIncludeInDeck(player))

    def test_min(self):
        self.RunCases("min_test_folder")

    def test_all(self):
        self.RunCases("all")

    def test_world_package_exports_real_class(self):
        import importlib
        import sys

        sys.modules.pop('game.world', None)
        sys.modules.pop('game.world.world', None)
        import game.world as world_pkg

        # Simulate the star-import path used during partial bootstrap; it must not
        # resolve to the placeholder type that would later fail with TypeError.
        namespace = {}
        exec('from game.world import *', namespace)

        world_type = namespace['World']
        self.assertEqual(world_type.__module__, 'game.world.world')
        self.assertTrue(callable(world_type))
        self.assertIs(world_type, importlib.import_module('game.world.world').World)

    def test_ability_type_placeholder_resolves_real_enum(self):
        namespace = {}
        exec('from core import *', namespace)

        ability_type = namespace['AbilityType']
        resolved_rule = ability_type.Rule
        self.assertEqual(resolved_rule.__class__.__name__, 'AbilityType')
        self.assertTrue(hasattr(resolved_rule, 'flags'))
        self.assertIs(resolved_rule, __import__('game.ability.ability_type', fromlist=['AbilityType']).AbilityType.Rule)

        timing_priority = namespace['TimingPriority']
        self.assertEqual(list(timing_priority), list(__import__('game.ability.ability_type', fromlist=['TimingPriority']).TimingPriority))
        self.assertIs(timing_priority.Rule, __import__('game.ability.ability_type', fromlist=['TimingPriority']).TimingPriority.Rule)

        final_type = namespace['FinalType']
        actual_final_type = __import__('game.card.face.base.final_type', fromlist=['FinalType']).FinalType
        self.assertTrue(isinstance(object.__new__(actual_final_type), final_type))
        self.assertTrue(issubclass(actual_final_type, final_type))

        has_cost = namespace['HasCost']
        self.assertTrue(hasattr(has_cost, 'IsType'))
        self.assertTrue(callable(has_cost.IsType))

    def test_ability_factory_star_import_resolves_runtime_factory(self):
        namespace = {}
        exec('from game.ability.factory import *', namespace)

        self.assertIn('AbilityFactory', namespace)
        self.assertIs(namespace['AbilityFactory'], __import__('game.ability.factory.ability_factory', fromlist=['AbilityFactory']).AbilityFactory)

    def test_pack_star_import_exposes_condition2_for_card_abilities(self):
        module = __import__('cards.pack.scw.scarlet_witch.15023', fromlist=['GetAbilities'])
        abilities = module.GetAbilities()
        self.assertTrue(abilities)
        self.assertTrue(hasattr(__import__('game.ability.condition.condition2', fromlist=['Condition2']).Condition2, 'ThisIsTrigger'))
        self.assertTrue(any(getattr(ability, 'conditions', None) for ability in abilities))

    def test_attribute_star_import_exposes_ability_factory(self):
        namespace = {}
        exec('from game.card.face.attribute import *', namespace)
        self.assertIn('AbilityFactory', namespace)
        self.assertIs(namespace['AbilityFactory'], __import__('game.ability.factory.ability_factory', fromlist=['AbilityFactory']).AbilityFactory)
        self.assertIs(namespace['HasCost'], __import__('game.card.face.attribute.has_cost', fromlist=['HasCost']).HasCost)
        self.assertTrue(callable(namespace['HasCost'].IsType))
        self.assertTrue(namespace['HasCost'].IsType(__import__('game.card.face.attribute.has_cost', fromlist=['HasCost']).HasCost))

    def test_has_uses_module_has_runtime_ability_factory(self):
        module = __import__('game.card.face.attribute.has_uses', fromlist=['HasUses'])
        self.assertIn('AbilityFactory', module.HasUses.GetAbilities.__code__.co_names)
        self.assertIn('game.ability.factory', module.HasUses.GetAbilities.__code__.co_names)

    def test_set_destroyed_after_uses_runtime_message_namespace(self):
        from types import SimpleNamespace
        from game.effect.effect import Effect

        effect = object.__new__(Effect)
        effect.is_temp = True
        effect.this = SimpleNamespace(effect=SimpleNamespace())
        effect.world = SimpleNamespace(round_id=0)
        effect.ability = SimpleNamespace(flags=SimpleNamespace())

        registered = []
        def register_temp(ability, unregister_after_exec=True):
            registered.append(ability)
            return []
        effect.this.effect.RegisterTemp = register_temp

        end_event = object()
        until_event = SimpleNamespace(end_event=end_event)
        until_event.pre_message = until_event
        effect.SetDestroyedAfter(False, until_after_event=until_event)

        condition = registered[-1].conditions[0]
        message = SimpleNamespace(CastTo=lambda cls: SimpleNamespace(pre_message=until_event))
        self.assertTrue(condition(effect, message))

    def test_effect_set_has_spell_in_phase_uses_runtime_trigger_message(self):
        from types import SimpleNamespace
        from game.effect.effect import Effect

        effect = object.__new__(Effect)
        effect.ability = SimpleNamespace(
            flags=SimpleNamespace(
                is_rule=False,
                is_statistics=False,
                is_interrupt=True,
                is_response=False,
                is_resource=False,
                is_when_completed=False,
                is_when_reveal=False,
                is_when_defeated=False,
                is_setup=False,
                is_boost=False,
                is_special=False,
                is_action=False,
                is_nonkeyword=False,
            ),
            when='test_event',
        )
        effect.context = SimpleNamespace(bind_message=None)
        effect.this = SimpleNamespace(effect=SimpleNamespace(global_effects=[], local_effects=[], given_effects=[]))
        effect.world = SimpleNamespace(rule=SimpleNamespace(disable_limit_once=False), stat=SimpleNamespace(RecordEffect=lambda *args, **kwargs: None, RecordEffectWithPlayer=lambda *args, **kwargs: None))
        effect.GetBindMessage = lambda event: SimpleNamespace(once_per_event_effects=[])

        self.assertIsNone(effect.SetHasSpellInPhase())

    def test_player_ask_uses_runtime_select_namespace(self):
        import game.player.model.player_ask as player_ask
        self.assertTrue(hasattr(player_ask, 'Select'))
        self.assertTrue(callable(player_ask.Select.From))

    def test_attack_module_uses_runtime_unused_binding(self):
        module = __import__('game.card.face.attribute.can_attack', fromlist=['AttackProperty'])
        self.assertTrue(hasattr(module, 'Unused'))
        self.assertIs(module.Unused, __import__('core', fromlist=['Unused']).Unused)

    def test_ability_defense_condition_uses_runtime_attacker_message_binding(self):
        from types import SimpleNamespace
        from game.ability.ability import Ability
        from game.ability.ability_type import AbilityType
        from game.message import Message

        ability = Ability(
            AbilityType.Interrupt,
            Message.WhenUnitWouldAttack,
            [],
            lambda effect, message: None,
        )
        ability.SetLabel('defense')
        ability.Initialize(SimpleNamespace())

        condition = next(c for c in ability.conditions if getattr(c, '__name__', '') == 'can_defense_attack')
        self.assertTrue(condition(SimpleNamespace(), SimpleNamespace(attacker=None)))

    def test_search_internal_uses_runtime_select_namespace(self):
        module = __import__('game.operate.search_internal', fromlist=['SearchInternal'])
        self.assertTrue(hasattr(module, 'Select'))
        self.assertTrue(callable(module.Select.From))

    def test_ability_factory_star_import_exposes_cost_func(self):
        namespace = {}
        exec('from game.ability.factory import *', namespace)

        self.assertIn('CostFunc', namespace)
        self.assertIs(namespace['CostFunc'], __import__('game.ability.cost_func', fromlist=['CostFunc']).CostFunc)

    def test_ability_factory_resource_module_has_runtime_cost_func_binding(self):
        module = __import__('game.ability.factory.resources', fromlist=['AbilityFactoryResources'])
        self.assertTrue(hasattr(module, 'CostFunc'))
        self.assertIs(module.CostFunc, __import__('game.ability.cost_func', fromlist=['CostFunc']).CostFunc)
        self.assertTrue(callable(module.CostFunc.Custom))

    def test_the_best_offense_is_constant(self):
        from game.ability.ability_type import AbilityType
        module = __import__('cards.pack.fne.60052', fromlist=['GetAbilities'])
        ability_types = [ability.type for ability in module.GetAbilities()]
        self.assertIn(AbilityType.NonKeyword, ability_types)
        self.assertNotIn(AbilityType.HeroInterrupt, ability_types)

    def test_upgrade_cards_accept_def_printed_values(self):
        from cards.paper import Paper
        from game.card.face.card_type.upgrade import Upgrade

        paper = Paper(
            card_id='60038',
            pic_id='',
            type='Upgrade',
            is_unique=False,
            name='Innate Reflexes',
            subtitle='',
            desc={'DEF': '1'},
            traits=[],
            pack='fne',
            set_name='Fear No Evil',
            text='Your hero gets +1 DEF.'
        )
        upgrade = Upgrade(paper)
        upgrade.InitPrintedValue('DEF', '1')
        self.assertEqual(upgrade.printed_defense, 1)

    def test_attachment_factory_has_runtime_select_namespace(self):
        module = __import__('game.ability.factory.attachment', fromlist=['AbilityFactoryAttachment'])
        self.assertTrue(hasattr(module, 'AbilityFactoryAttachment'))
        self.assertTrue(callable(module.AbilityFactoryAttachment.AttachToFaceWhenPutIntoPlay))
        self.assertTrue(hasattr(__import__('game.selector', fromlist=['Select']), 'Select'))

    def test_cost_func_module_has_runtime_selectors(self):
        module = __import__('game.ability.cost_func', fromlist=['CostFunc'])
        self.assertTrue(hasattr(module, 'Select'))
        self.assertTrue(hasattr(module, 'Selector'))
        self.assertIsNotNone(module.Select.From)

    def test_ability_module_has_runtime_select_namespace(self):
        module = __import__('game.ability.ability', fromlist=['SELECT'])
        self.assertTrue(hasattr(module, 'SELECT'))
        self.assertTrue(hasattr(module.SELECT, 'HELPER_TYPE'))

    def test_version_exists_before_engine_initialize(self):
        from engine.lib.version import Ver

        self.assertTrue(hasattr(Ver, 'version'))
        self.assertIsNotNone(Ver.version)
        self.assertTrue(str(Ver.version).count('.') >= 3)

    def test_identity_uses_real_final_type_base(self):
        from game.card.face.card_type.identity import Hero, AlterEgo

        self.assertTrue(any(base.__module__ == 'game.card.face.base.final_type' for base in Hero.__bases__))
        self.assertTrue(any(base.__module__ == 'game.card.face.base.final_type' for base in AlterEgo.__bases__))

    def test_profile_profile(self):
        self.RunCases("profile_folder", release=False, profile=True)

    def test_profile_debug(self):
        self.RunCases("profile_folder", release=False, profile=False)

    def test_profile_release(self):
        self.RunCases("profile_folder")


