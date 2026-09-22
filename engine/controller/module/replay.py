from __future__ import annotations

from typing import TYPE_CHECKING
from collections import Counter

from core import *
from engine.log import Log
from game.scene.replay import *
from game.world import *
from engine.config import ConfigVariables

if TYPE_CHECKING:
    from engine.controller.manager import ControllerManager

CATEGORY_NAME = "REPLAY"
DISABLE_CRC_ERROR_ASSERT    = ConfigVariables.Bool('disable_crc_error_assert', False)
CRC_IGNORE_IDS              = ConfigVariables.ListInt('crc_ignore_ids', [])
DEBUG_REPLAY_PUSH           = ConfigVariables.Bool('debug_replay_push', True)
REPLAY_CRC_DEBUG_WINDOW     = ConfigVariables.Int('replay_crc_debug_window', 6)

class InputModule:

    def __init__(self, manager: 'ControllerManager') -> None:
        self.replay_inputs: List['OperationDescriptor'] = []
        self.history_inputs: List['OperationDescriptor'] = []

        self.current_step_id = 0
        self.replay_step_id = 0

        self.is_updated = False

        self.calculated_crc: List[str] = []

        self.is_replay: bool = False

        self.break_on: List[int] = []
        self.push_count = 0

        self.manager = manager

    def Clean(self):
        self.replay_inputs = []
        self.history_inputs = []

        self.current_step_id = 0
        self.replay_step_id = 0
        self.is_updated = False
        self.calculated_crc = []
        self.push_count = 0

    def Clear(self):
        self.break_on = []

    def SetReplayInputs(self, inputs: List['OperationDescriptor']):
        self.replay_inputs = inputs

    def SetIsReplay(self, replay: bool):
        self.is_replay = replay

    def SetBreakOn(self, break_on: List[int]):
        self.break_on = break_on

    def PrintStepID(self) -> str:
        from colorama import Fore, Style
        # replay_inputs_max_size = self.GetReplayOperationLen()
        # return f'{Fore.RED}#{Style.RESET_ALL}{self.current_step_id} ({controller_manager.last_turn_start_step_id} | {controller_manager.undo.last_step}) /{replay_inputs_max_size if replay_inputs_max_size > 0 else ""}'
        return f'{Fore.RED}(#{self.current_step_id} / {len(self.replay_inputs)}){Style.RESET_ALL}'

    ################################################################################
    #
    def Push(self, operation: 'OperationDescriptor'):
        self.history_inputs.append(operation)
        self.current_step_id += 1
        self.replay_step_id += 1
        self.push_count += 1

        if DEBUG_REPLAY_PUSH.value:
            effect_id = operation.effect.id if operation.effect and operation.effect.id else ""
            event_name = operation.event if operation.event else ""
            Log.Debug(
                CATEGORY_NAME,
                f"PUSH#{self.push_count} step={self.current_step_id} replay={self.replay_step_id} event={event_name} effect={effect_id}"
            )

        if self.current_step_id in self.break_on:
            self.manager.skip.SetIsSkipping(False)

    def Pop(self):
        self.history_inputs.pop()
        self.current_step_id -= 1
        self.replay_step_id -= 1

    def _format_op(self, op: 'OperationDescriptor') -> str:
        effect_id = op.effect.id if op.effect and op.effect.id else ""
        return f"step={op.step} event={op.event} effect={effect_id}"

    def _format_recent_ops(self, size: int) -> str:
        if size <= 0:
            return ""
        ops = self.history_inputs[-size:]
        if not ops:
            return ""
        text = "Recent history operations:\n"
        for op in ops:
            text += f"- {self._format_op(op)}\n"
        return text

    def _format_upcoming_ops(self, size: int) -> str:
        if size <= 0:
            return ""
        begin = self.replay_step_id
        end = min(self.replay_step_id + size, len(self.replay_inputs))
        ops = self.replay_inputs[begin:end]
        if not ops:
            return ""
        text = "Upcoming replay operations:\n"
        for op in ops:
            text += f"- {self._format_op(op)}\n"
        return text

    def _format_card_info(self, key: int) -> str:
        from engine import Engine

        game = Engine.game
        if not game or not game.world:
            return ""

        card = game.world.object_manager.card_dict.get(key, None)
        if not card:
            return ""

        face = getattr(card, 'face', None)
        if not face:
            return ""

        card_name = str(face)
        paper = getattr(face, 'paper', None)
        card_id = getattr(paper, 'card_id', "")
        area = getattr(card, 'area', None)
        area_name = str(area) if area else ""
        return f"{card_name} [{card_id}] @{area_name}"

    def _is_equivalent_deck_position_swap(self, da: Dict[int, int], db: Dict[int, int], diff_ids: Sequence[int]) -> bool:
        """Treat top/bottom marker swaps among identical cards in the same area as equivalent state."""
        if not diff_ids:
            return False

        from engine import Engine

        game = Engine.game
        if not game or not game.world:
            return False

        world = game.world
        groups: Dict[Tuple[str, str], List[int]] = {}
        allowed_values = {None, -3, -4}

        for key in diff_ids:
            card = world.object_manager.card_dict.get(key, None)
            if not card:
                return False

            face = getattr(card, 'face', None)
            paper = getattr(face, 'paper', None) if face else None
            card_id = getattr(paper, 'card_id', None)
            area = getattr(card, 'area', None)
            area_name = str(area) if area else ""

            if not card_id or not area_name:
                return False

            a_value = da.get(key, None)
            b_value = db.get(key, None)
            if a_value not in allowed_values or b_value not in allowed_values:
                return False

            groups.setdefault((area_name, card_id), []).append(key)

        # Every differing card must be in a group where the value multiset matches.
        # This means object ids may differ, but equivalent cards keep the same aggregate state.
        for grouped_ids in groups.values():
            read_values = Counter(da.get(k, None) for k in grouped_ids)
            curr_values = Counter(db.get(k, None) for k in grouped_ids)
            if read_values != curr_values:
                return False

        covered = sum(len(ids) for ids in groups.values())
        return covered == len(diff_ids)

    def GetReplayOperation(self, is_puzzle: bool, *, check_crc: bool=True) -> Tuple['OperationDescriptor|None', bool]:
        from engine import Engine
        self.is_updated = False

        if self.GetReplayOperationLen() > self.replay_step_id:
            replay_input = self.replay_inputs[self.replay_step_id]
            if is_puzzle or not check_crc:
                return replay_input, True
            # return replay_input

            # Check crc
            if replay_input.crc == "":
                Log.Warn(CATEGORY_NAME, "Miss CRC")
            if replay_input.crc and \
                self.calculated_crc[0] != replay_input.crc and \
                self.calculated_crc[1] != replay_input.crc and \
                self.calculated_crc[2] != replay_input.crc and \
                not Engine.game.controller_manager.console.debug_cmds:

                disable_assert = DISABLE_CRC_ERROR_ASSERT.value

                import ast
                da = ast.literal_eval(replay_input.crc)
                if self.manager.game.scene.version == '0.5.9.4':
                    db = ast.literal_eval(self.calculated_crc[1])
                else:
                    db = ast.literal_eval(self.calculated_crc[0])

                # Get the union of keys from both dictionaries
                all_keys = sorted(set(da) | set(db))

                diff_text = ""
                diff_ids: List[int] = []
                # Compare and print
                def get_text(num: int|None) -> str:
                    if num == None:
                        return '-'
                    # if num == 0:
                    #     return '0'
                    if num >= 0:
                        return str(num)
                    if num == -2:
                        return 'Hand'
                    if num == -3:
                        return 'Top'
                    if num == -4:
                        return 'Btm'
                    # This happens when a unit has negative health
                    # assert False
                    return str(num)
                def get_diff_text(a: int|None, b: int|None) -> str:
                    if a == None:
                        a = 0
                    if b == None:
                        b = 0
                    if a < 0 or b < 0:
                        return ''
                    if a == b:
                        return ''
                    return "{:+}".format(b-a)

                for key in all_keys:
                    a_value = da.get(key, None)
                    b_value = db.get(key, None)
                    if a_value != b_value:
                        diff_ids.append(key)
                        card_info = self._format_card_info(key)
                        diff_text += "c{:<4}| {:<4} | {:<4} | {:<3} | {}\n".format(
                            key,
                            get_text(a_value),
                            get_text(b_value),
                            get_diff_text(a_value, b_value),
                            card_info,
                        )

                if self._is_equivalent_deck_position_swap(da, db, diff_ids):
                    Log.Warn(CATEGORY_NAME, f"Replay CRC tolerated equivalent deck-position swap at step #{self.current_step_id}")
                    return replay_input, True

                if not disable_assert:
#                     tip_info = """
#  N : player id + exhaust + health + states + atk + thw + def + rec + counter + scheme + ...
# -2 : in hand
# -3 : deck top
# -4 : deck bottom

#  Key | Read\t| Curr
# """
                    tip_info = f""" Key | Read | Curr | (#{self.current_step_id} / {len(self.replay_inputs)})
"""
                    context_window = max(REPLAY_CRC_DEBUG_WINDOW.value, 0)
                    expected_op = self.replay_inputs[self.replay_step_id] if self.replay_step_id < len(self.replay_inputs) else None
                    expected_text = f"Expected replay operation:\n- {self._format_op(expected_op)}\n" if expected_op else ""
                    recent_text = self._format_recent_ops(context_window)
                    upcoming_text = self._format_upcoming_ops(context_window)
                    Log.Assert(CATEGORY_NAME, f'{tip_info}{diff_text}{expected_text}{recent_text}{upcoming_text}')

                from game.test import Test
                if Engine.in_unit_test:
                    Engine.SaveCrash()
                if Test.IsInTesting():
                    # DebugBreak()
                    if not disable_assert:
                        from core.lib.beep import Beep
                        Beep.Warning()
                        return replay_input, False
                    pass
                if all(x for x in diff_ids if x in CRC_IGNORE_IDS.value):
                    return replay_input, True
                else:
                    return replay_input, False
            return replay_input, True
        else:
            return None, True

    def GetReplayOperationLen(self) -> int:
        return len(self.replay_inputs)

    def UpdateReplayStepId(self, diff: int):
        self.replay_step_id += diff
        self.is_updated = True

