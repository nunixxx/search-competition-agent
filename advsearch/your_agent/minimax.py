import random
from typing import Tuple, Callable

def alphabeta(state, depth, alpha, beta, maximizing, root_player, max_depth, eval_func):
    """
    Algoritmo minimax com poda alfa-beta.
    :param state: estado atual do jogo
    :param depth: profundidade atual na árvore de busca
    :param alpha: valor alfa para poda
    :param beta: valor beta para poda
    :param maximizing: se este é um nó maximizador
    :param root_player: o jogador que iniciou a busca
    :param max_depth: profundidade máxima de busca (-1 = ilimitada)
    :param eval_func: função de avaliação para estados terminais/folha
    :return: valor de utilidade do estado
    """
    if state.is_terminal():
        return eval_func(state, root_player)

    if max_depth != -1 and depth >= max_depth:
        return eval_func(state, root_player) 

    if maximizing:
        value = float('-inf')
        for move in state.legal_moves():
            child = state.next_state(move)
            value = max(value, alphabeta(child, depth + 1, alpha, beta, False, root_player, max_depth, eval_func))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in state.legal_moves():
            child = state.next_state(move)
            value = min(value, alphabeta(child, depth + 1, alpha, beta, True, root_player, max_depth, eval_func))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    # The player for whom we are calculating the move
    root_player = state.player 

    # Find the best move
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # Shuffle legal moves to add some variability in case of ties
    for move in state.legal_moves():
        child = state.next_state(move)
        value = alphabeta(child, 0, alpha, beta, False, root_player, max_depth, eval_func)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)

    return best_move