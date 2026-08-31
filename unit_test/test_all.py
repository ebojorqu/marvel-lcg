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
            @staticmethod
            def IsType(obj):
                return isinstance(obj, FakePlayer)

        class FakeIdentity:
            def __init__(self, controller):
                self._controller = controller
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

        class FakeUpgrade(FakeIdentity):
            def __init__(self, bind_face):
                super().__init__(bind_face._control_by)
                self.bind_face = bind_face
            def GetBindFace(self):
                return self.bind_face

        old_player = player_module.Player
        old_identity = card_type_module.Identity
        old_upgrade = card_type_module.Upgrade
        old_event = card_type_module.Event
        try:
            player_module.Player = FakePlayer
            card_type_module.Identity = FakeIdentity
            card_type_module.Upgrade = FakeUpgrade
            card_type_module.Event = type('FakeEvent', (), {})

            attack_target_player = FakePlayer(FakeIdentity(None))
            defending_player = FakePlayer(FakeIdentity(None))
            identity = FakeIdentity(attack_target_player)
            effect = SimpleNamespace(
                this=FakeFace(defending_player),
                initiator=attack_target_player,
                context=SimpleNamespace(ask_player=defending_player),
            )

            self.assertTrue(Condition.ThisIsYou(effect, identity))

            ally_face = FakeFace(attack_target_player)
            self.assertTrue(Condition.CheckWhichCard("YouControlAlly", [ally_face], effect))
        finally:
            player_module.Player = old_player
            card_type_module.Identity = old_identity
            card_type_module.Upgrade = old_upgrade
            card_type_module.Event = old_event

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

    def test_ability_factory_star_import_exposes_cost_func(self):
        namespace = {}
        exec('from game.ability.factory import *', namespace)

        self.assertIn('CostFunc', namespace)
        self.assertIs(namespace['CostFunc'], __import__('game.ability.cost_func', fromlist=['CostFunc']).CostFunc)

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


