"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # counts the number of empty spaces
    empty_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_count += 1

    # if the number of empty spaces is even, it's O's turn
    if empty_count % 2 == 0: 
        return O
    
    # if the number of empty spaces is odd, it's X's turn (because X always goes first)
    elif empty_count % 2 == 1: 
        return X
    
    return None

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    # if there is empty spaces on the board, it adds the coordinates of those spaces to the set of possible actions
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    # makes a deepcopy of the board to avoid mutating the original board
    result_board = copy.deepcopy(board) 

    if (i not in [0, 1, 2] or 
        j not in [0, 1, 2] or
        board[i][j] is not EMPTY): # checks for invalid actions
        raise Exception("Invalid action")
    
    if player(board) == X: # if it's X's turn
        result_board[i][j] = X
    else: # if it's O's turn
        result_board[i][j] = O
    
    return result_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Row major
    for i in range(3):
        x_count = 0
        o_count = 0
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            if board[i][j] == O:
                o_count += 1
        if x_count == 3:
            return X
        elif o_count == 3:
            return O

    # Column major   
    for j in range(3):
        x_count = 0
        o_count = 0
        for i in range(3):
            if board[i][j] == X:
                x_count += 1
            if board[i][j] == O:
                o_count += 1
        if x_count == 3:
            return X
        elif o_count == 3:
            return O

    # Diagonal major
    if (board[0][0] == X and 
        board[1][1] == X and 
        board[2][2] == X):
        return X
    elif (board[0][0] == O and 
          board[1][1] == O and 
          board[2][2] == O):
        return O
    
    # Diagonal minor
    if (board[0][2] == X and
        board[1][1] == X and 
        board[2][0] == X):
        return X
    elif (board[0][2] == O and
          board[1][1] == O and 
          board[2][0] == O):
        return O

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None: # there is a winner
        return True
    
    # if there are still empty spaces on the board, the game is not over
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: 
                return False
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): # if there is a terminal board then there are no possible actions
        return None
 
    if player(board) == X:
        action = max_value(board)[1] # X is the maximizing player
    else: 
        action = min_value(board)[1] # O is the minimizing player

    return action

    raise NotImplementedError


def max_value(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the optimal action and value for the maximizing player on the board (with alpha-beta pruning).
    """
    if terminal(board):
        # returns the value of the board once a terminal state is reached (end of the branch)
        return [utility(board), None]
    
    v = -math.inf # initializes v to negative infinity
    best_action = None
    for action in actions(board):
        # recursively calls min_value to analyze the resulting board
        new_v = min_value(result(board, action), alpha, beta)[0]
        
        if new_v > v: # checks to see if the new value is better than the current best value
            v = new_v
            best_action = action

        alpha = max(alpha, v) # alpha stores the best value for the maximizing player found so far
        if beta <= alpha: # prunes the remaining branches if the minimizing player has a better option already
            break
        
    return [v, best_action]


def min_value(board, alpha=-math.inf, beta=math.inf):
    """
    Returns the optimal action and value for the minimizing player on the board (with alpha-beta pruning).
    """
    if terminal(board):
        # returns the value of the board once a terminal state is reached (end of the branch)
        return [utility(board), None]
    
    v = math.inf # initializes v to positive infinity
    best_action = None
    for action in actions(board):
        # recursively calls max_value to analyze the resulting board
        new_v = max_value(result(board, action), alpha, beta)[0]
        
        if new_v < v: # checks to see if the new value is better than the current best value
            v = new_v
            best_action = action

        beta = min(beta, v) # beta stores the best value for the minimizing player found so far
        if beta <= alpha: # prunes the remaining branches if the maximizing player has a better option already
            break
            
    return [v, best_action]
