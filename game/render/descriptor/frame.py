from core import *

@dataclass
class FrameDescriptor:
    render_id           : int
    game_id             : int
    ask_players         : List[int]
    remaining_time      : float
    max_timeout         : float
    notify_texts        : List[str]
    debug_message       : str
    current_step_id     : int
    max_replay_step_id  : int
    undo_target_step    : int
    undo_target_is_fallback: bool
    player_id           : int
    total_players       : int
    # is_skipping         : bool

