import random
from typing import Tuple
from ..tttm.board import Board
from .minimax import minimax_move
from ..tttm.gamestate import GameState

"""
    Retorna uma jogada calculada pelo algoritmo minimax para o estado de jogo fornecido.
    :param state: estado para fazer a jogada
    :return: tupla (int, int) com as coordenadas x, y da jogada (lembre-se: 0 é a primeira linha/coluna)
"""

def make_move(state: GameState) -> Tuple[int, int]:
    return minimax_move(state, -1, utility)

"""
    Retorna a utilidade de um estado (terminal) 
"""
def utility(state, player: str) -> float:
    winner = state.winner()
    if winner == player:
        return 1.0
    elif winner is None:
        return 0.0
    else:
        return -1.0
