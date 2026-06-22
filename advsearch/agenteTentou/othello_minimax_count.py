import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

MAX_DEPTH = 4


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    legal_moves = list(state.legal_moves())
    if not legal_moves:
        # No legal moves available for this player in a non-terminal state should not happen,
        # but we keep a fallback for safety.
        raise ValueError('No legal moves available')

    best_move = minimax_move(state, MAX_DEPTH, evaluate_count)
    if best_move is None:
        return random.choice(legal_moves)

    return best_move


def evaluate_count(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the number of pieces of each color.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    opponent = Board.opponent(player)
    player_count = state.board.num_pieces(player)
    opponent_count = state.board.num_pieces(opponent)

    if state.is_terminal():
        return float(player_count - opponent_count)

    return float(player_count - opponent_count)
