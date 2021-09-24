"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None

winning_shapes = [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(1, 0), (1, 1), (1, 2)],
                  [(0, 1), (1, 1), (2, 1)], [(2, 0), (2, 1), (2, 2)], [(0, 2), (1, 2), (2, 2)],
                  [(0, 0), (1, 1), (2, 2)], [(2, 0), (1, 1), (0, 2)]]


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def count_board(board):
    """Counts the difference between how many moves each side has made on the given board

    if X is max and O is min, 1 means there is more X moves, 0 means balance
    (in theory any other score is impossible)
    """
    scores = {X: 0, O: 0}
    for row in board:
        for sq in row:
            if sq in scores:
                scores[sq] += 1
    return scores[X] - scores[O]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    score = count_board(board)
    if score > 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for y in range(3):
        for x in range(3):
            if board[y][x] == EMPTY:
                moves.append((y, x))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check each shape
    for shape in winning_shapes:
        score = 0
        for coord in shape:
            sq = board[coord[0]][coord[1]]
            if sq == O:
                score -= 1
            if sq == X:
                score += 1
        if score == 3:
            return X
        if score == -3:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    if actions(board):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == O:
        return -1
    if win == X:
        return 1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    best_move = bestmove(board, 0)[1]
    return best_move


def bestmove(board, ups_best):
    who_plays = player(board)
    available_moves = actions(board)

    best_move = None  # best move found so far
    best_value = -2 if who_plays == X else 2  # value of the best move, initial placeholder depends on who plays

    # consider all available moves
    for move in available_moves:
        # check consequence of making this move
        consq = result(board, move)
        # if the board is terminal, it's value is it's utility
        if terminal(consq):
            move_value = utility(consq)
        else:
            move_value = bestmove(consq, best_value)[0]

        # compare the value of this move to the one at the top
        if (who_plays == X and move_value > best_value) or (who_plays == O and move_value < best_value):
            best_value = move_value
            best_move = move

            # pruning (act only when the best value changes)
            if (who_plays == X and best_value > ups_best) or (who_plays == O and best_value < ups_best):
                return best_value, best_move

    # the best value that the current player can achieve
    return best_value, best_move





