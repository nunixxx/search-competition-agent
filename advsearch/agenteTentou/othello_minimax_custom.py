import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from .othello_minimax_mask import EVAL_TEMPLATE

MAX_DEPTH = 4

def make_move(state) -> Tuple[int, int]:
    legal_moves = list(state.legal_moves())
    if not legal_moves:
        raise ValueError('No legal moves available')

    best_move = minimax_move(state, MAX_DEPTH, evaluate_custom)
    if best_move is None:
        return random.choice(legal_moves)

    return best_move


def evaluate_custom(state, player: str) -> float:
    opponent = Board.opponent(player)

    if state.is_terminal():
        winner = state.winner()
        if winner == player:
            return 10000.0
        elif winner is None:
            return 0.0
        else:
            return -10000.0

    n_empty = state.board.piece_count[Board.EMPTY]

    mask_score = 0
    for y in range(8):
        for x in range(8):
            piece = state.board.tiles[y][x]
            if piece == player:
                mask_score += EVAL_TEMPLATE[y][x]
            elif piece == opponent:
                mask_score -= EVAL_TEMPLATE[y][x]

    player_mobility = len(state.board.legal_moves(player))
    oponent_mobility = len(state.board.legal_moves(opponent))
    mobility = player_mobility - oponent_mobility

    player_frontier = 0
    oponent_frontier = 0
    for y in range(8):
        for x in range(8):
            piece = state.board.tiles[y][x]
            if piece == Board.EMPTY:
                continue
            for dy, dx in Board.DIRECTIONS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < 8 and 0 <= nx < 8 and state.board.tiles[ny][nx] == Board.EMPTY:
                    if piece == player:
                        player_frontier += 1
                    elif piece == opponent:
                        oponent_frontier += 1
                    break
    frontier = oponent_frontier - player_frontier

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_score = 0
    for x, y in corners:
        piece = state.board.tiles[y][x]
        if piece == player:
            corner_score += 1
        elif piece == opponent:
            corner_score -= 1

    if n_empty > 40:
        w_mask = 1.0
        w_mobility = 150
        w_frontier = 10
        w_corner = 500
    elif n_empty > 20:
        w_mask = 1.0
        w_mobility = 350
        w_frontier = 30
        w_corner = 2000
    else:
        w_mask = 0.5
        w_mobility = 1000
        w_frontier = 10
        w_corner = 5000

    score = (w_mask * mask_score
             + w_mobility * mobility
             + w_frontier * frontier
             + w_corner * corner_score)

    return float(score)
