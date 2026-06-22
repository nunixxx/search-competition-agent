import random
import time
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move


def make_move(state) -> Tuple[int, int]:
    if state.game_name == 'Othello':
        return othello_iterative_deepening(state, time_limit=4.5)
    else:
        from .tttm_minimax import make_move as tttm_make_move
        return tttm_make_move(state)


def othello_iterative_deepening(state, time_limit=4.5):
    legal_moves = list(state.legal_moves())
    if not legal_moves:
        return None

    from .othello_minimax_custom import evaluate_custom

    n_empty = state.board.piece_count[Board.EMPTY]

    if n_empty <= 12:
        result = minimax_move(state, -1, evaluate_custom)
        if result is not None:
            return result
        return random.choice(legal_moves)

    best_move = random.choice(legal_moves)
    start = time.monotonic()
    last_elapsed = 0.0

    for depth in range(1, 31):
        elapsed = time.monotonic() - start
        remaining = time_limit - elapsed
        if remaining <= 1.0:
            break
        if last_elapsed > 0 and remaining < last_elapsed * 4:
            break

        t0 = time.monotonic()
        result = minimax_move(state, depth, evaluate_custom)
        last_elapsed = time.monotonic() - t0

        if result is not None:
            best_move = result

    return best_move
