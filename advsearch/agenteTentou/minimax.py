import time
import random
from typing import Tuple, Callable, List
from ..othello.board import Board

_start_time = None
_time_limit = None

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
    """
    Algoritmo minimax com poda alfa-beta e verificação de tempo limite via condicional.
    """
    global _start_time, _time_limit
    
    if _start_time is not None and _time_limit is not None:
        if time.time() - _start_time >= _time_limit:
            return 0 

    if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
        return eval_func(state, root_player)

    legal_moves = state.legal_moves()

    if not legal_moves:
        try:
            opponent = state.board.opponent(state.player)
        except Exception:
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
            
            if _start_time and _time_limit and time.time() - _start_time >= _time_limit:
                return 0.0
                
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
            
            if _start_time and _time_limit and time.time() - _start_time >= _time_limit:
                return 0.0
                
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

    if max_depth > 0:
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

    global _start_time, _time_limit
    _start_time = time.time()
    _time_limit = 4.5 

    best_move = random.choice(legal_moves)
    current_depth = 1

    while True:
        move_at_depth = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        timed_out = False

        ordered_moves = order_moves(state, legal_moves, root_player, reverse=True)

        for move in ordered_moves:
            child = state.next_state(move)
            next_maximizing = True if child.player == root_player else False
            value = alphabeta(child, 1, alpha, beta, next_maximizing, root_player, current_depth, eval_func)
            
            if time.time() - _start_time >= _time_limit:
                timed_out = True
                break
            
            if value is None:
                continue

            if value > best_value:
                best_value = value
                move_at_depth = move
            alpha = max(alpha, best_value)

        if timed_out:
            break

        if move_at_depth is not None:
            best_move = move_at_depth

        if current_depth >= 64 or state.is_terminal():
            break

        current_depth += 1

    _start_time = None
    _time_limit = None
    
    return best_move