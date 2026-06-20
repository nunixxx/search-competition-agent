import random
import time
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from ..timer import FunctionTimer
from .minimax import minimax_move
from .tttm_minimax import make_move

def make_move(state) -> Tuple[int, int]:
    if state.game_name == 'Othello':
        return othello_iterative_deepening(state, time_limit=4.0)
    else:
        return make_move(state)


def othello_iterative_deepening(state, time_limit=4.0):
    legal_moves = list(state.legal_moves())
    if not legal_moves:
        return None

    from .othello_minimax_custom import evaluate_custom

    n_empty = state.board.piece_count[Board.EMPTY]

    # FINAL DE JOGO (<=12 vazios): busca profunda ou até o fim
    if n_empty <= 12:
        timer = FunctionTimer(minimax_move, (state, -1, evaluate_custom))
        result = timer.run(time_limit)
        if result is not None:
            return result
        return random.choice(legal_moves)

    # APROFUNDAMENTO ITERATIVO
    # Começa com uma jogada aleatória como fallback seguro
    best_move = random.choice(legal_moves)
    start = time.monotonic()

    for depth in range(1, 31):
        elapsed = time.monotonic() - start
        remaining = time_limit - elapsed
        if remaining <= 0.3:
            break

        timer = FunctionTimer(minimax_move, (state, depth, evaluate_custom))
        result = timer.run(remaining)

        if result is None:
            break
        best_move = result

    return best_move
