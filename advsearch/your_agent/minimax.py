from typing import Tuple, Callable, List
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

    # 
    if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
        return eval_func(state, root_player)

    legal_moves = state.legal_moves()

    if not legal_moves:
        # If the state is terminal or we've reached max depth, evaluate it.
        if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
            return eval_func(state, root_player)

        # Otherwise this is a "pass" situation in games like Othello:
        # the player has no legal moves but the game is not over —
        # pass the turn to the opponent and continue search.
        try:
            opponent = state.board.opponent(state.player)
        except Exception:
            # If we cannot determine opponent, fall back to evaluating.
            return eval_func(state, root_player)

        # If opponent has moves, create a pass state and recurse.
        if state.board.has_legal_move(opponent):
            pass_state = state.copy()
            pass_state.player = opponent
            return alphabeta(pass_state, depth + 1, alpha, beta, not maximizing, root_player, max_depth, eval_func)

        # Neither player has legal moves -> terminal
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
    legal_moves = list(state.legal_moves())

    if not legal_moves:
        return None

    # Find the best move
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # Order moves: best first for max node = descending from root_player's view
    legal_moves = order_moves(state, legal_moves, root_player, reverse=True)

    for move in legal_moves:
        child = state.next_state(move)
        
        next_maximizing = True if child.player == root_player else False
        
        value = alphabeta(child, 1, alpha, beta, next_maximizing, root_player, max_depth, eval_func)
        
        if value > best_value:
            best_value = value
            best_move = move
        
        alpha = max(alpha, best_value)

    return best_move