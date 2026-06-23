import random
from typing import Tuple, Callable
from ..othello.board import Board

def order_moves(state, moves, root_player, reverse=True):
    try:
        opp = Board.opponent(root_player)
        scored = []
        for move in moves:
            child = state.next_state(move)
            val = child.board.num_pieces(root_player) - child.board.num_pieces(opp)
            scored.append((val, move))
        scored.sort(key=lambda x: x[0], reverse=reverse)
        return [m for _, m in scored]
    except AttributeError:
        return list(moves)

def alphabeta(state, depth, alpha, beta, maximizing, root_player, max_depth, eval_func):
    if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
        return eval_func(state, root_player)

    legal_moves = state.legal_moves()

    if not legal_moves:
        try:
            opponent = state.board.opponent(state.player)
        except AttributeError:
            opponent = 'W' if state.player == 'B' else 'B'

        pass_state = state.copy()
        pass_state.player = opponent

        if pass_state.legal_moves():
            return alphabeta(pass_state, depth + 1, alpha, beta, not maximizing, root_player, max_depth, eval_func)
        
        return eval_func(state, root_player)

    if maximizing:
        legal_moves = order_moves(state, list(legal_moves), root_player, reverse=True)
        value = float('-inf')
        for move in legal_moves:
            child = state.next_state(move)
            next_maximizing = maximizing if child.player == state.player else not maximizing
            res = alphabeta(child, depth + 1, alpha, beta, next_maximizing, root_player, max_depth, eval_func)
            
            value = max(value, res)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        legal_moves = order_moves(state, list(legal_moves), root_player, reverse=False)
        value = float('inf')
        for move in legal_moves:
            child = state.next_state(move)
            next_maximizing = maximizing if child.player == state.player else not maximizing
            res = alphabeta(child, depth + 1, alpha, beta, next_maximizing, root_player, max_depth, eval_func)
            
            value = min(value, res)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Retorna a melhor jogada calculada pelo Minimax com Poda Alfa-Beta.
    """
    root_player = state.player 
    legal_moves = list(state.legal_moves())

    if not legal_moves:
        return None

    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    ordered_moves = order_moves(state, legal_moves, root_player, reverse=True)

    for move in ordered_moves:
        child = state.next_state(move)
        next_maximizing = True if child.player == root_player else False
        value = alphabeta(child, 1, alpha, beta, next_maximizing, root_player, max_depth, eval_func)
        
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)

    return best_move if best_move is not None else random.choice(legal_moves)