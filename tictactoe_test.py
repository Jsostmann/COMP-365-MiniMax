# Import module `copy` for function `deepcopy` to deeply copy an
# original (mutable) object to save the object from mutations
import math
import copy

X = 'X'
O = 'O'
EMPTY = None

def initial_state():
    """Returns starting state of the board"""
    return [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
            ]


def display(board, autoprint=False):
    """Displays the board nested list as
        a 3x3 matrix for board visualization
        """
    vis_board = ''
    
    for row in board:
        for playr in row:
            if playr is None:
                playr = ' '
            
            playr += ' '
            vis_board += playr
        
        vis_board += '\n'
    
    if autoprint:
        print(vis_board)
    
    return vis_board


def player(board):
    """Returns player who has the next turn on a board
        """
    
    global X, O
    
    # Initial values for every call of the function
    X_count = 0
    O_count = 0
    
    for row in board:
        for playr in row:
            if playr == X:
                X_count += 1
            
            elif playr == O:
                O_count += 1

    # `X` always starts first
    if O_count < X_count:
        return O
    
    return X


def actions(board):
    """Returns set of all possible actions
        (i, j) available on the board
        """
    
    global EMPTY
    
    action_set = set()
    
    for i, row in enumerate(board):
        for j, playr in enumerate(row):
            if playr is EMPTY:
                action_set.add((i, j))

    return action_set


def result(board, action):
    """Returns the board that results from
        making move (i, j) on the board.
        """
    
    global EMPTY
    
    if type(action) is not tuple or len(action) != 2:
        raise Exception('invalid action taken')

    # Using `deepcopy` to make a deepcopy of *board*
    # as duplication by slicing entire list and by
    # type conversion is not working poperly
    dup_board = copy.deepcopy(board)

    # Unpack the coordinates as `I` and `J`
    I, J = action
    
    # Check if place has not already been used
    if dup_board[I][J] is EMPTY:
       dup_board[I][J] = player(board)
    
    else:
        raise Exception('invalid action taken')

    return dup_board


def is_full(board):
    """Returns True if all places have been occupied, else returns False
        """
    
    global EMPTY
    
    for row in board:
        for playr in row:
            if playr is EMPTY:
                return False

    return True


def winner(board):
    """Returns the winner of the game, if there is one.
        """
    
    winr = None # Initial declaration to avoid errors if no winner found
    
    # Check diagonally
    if (board[1][1] == board[0][0] and board[0][0] == board[2][2])\
        or (board[1][1] == board[0][2] and board[0][2] == board[2][0]):
            winr = board[1][1]
            return winr

    for i in range(3):
        # Check each row for three-in-a-row
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            winr = board[i][1]
            break
        
        # Check each column for three-in-a-column
        elif board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            winr = board[1][i]
            break

    return winr


def terminal(board):
    """Returns True if game is over, False otherwise.
        """
    
    if winner(board) is None and not is_full(board):
        return False
    
    return True


def utility(board):
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """
    global X, O
    
    if terminal(board):
        winr = winner(board)
        
        if winr == X:
            util = 1
        
        elif winr == O:
            util = -1
        
        else:
            util = 0
        
        return util
    
    return None

def minimaxRec(board, isMaximizer):
    # if end state return 1 for max win -1 for min win and 0 for tie
    if utility(board) is not None:
        return utility(board)
    
    if isMaximizer == True:
        score = -math.inf
        for action in actions(board):
            newBoard = result(board, action)
            minPlayer = minimaxRec(newBoard, not isMaximizer)
            score = max(minPlayer,score)
        
        return score

    elif isMaximizer == False:
        score = math.inf
        for action in actions(board):
            newBoard = result(board, action)
            maxPlayer = minimaxRec(newBoard,not isMaximizer)
            score = min(maxPlayer, score)

        return score

def get_best_score(board, is_max_turn):
    """Returns the best value of values of all possible moves
        """
    #print(is_max_turn)

    if utility(board) is not None:
        return utility(board)
    
    scores = []
    # Recursively help `minimax` choose the best action
    # in `actions` of *board* by returning the best value
    for action in actions(board):
        rslt = result(board, action)
        scores.append(get_best_score(rslt, not is_max_turn))
    return max(scores) if is_max_turn else min(scores)

def minimax(board):
    
    if terminal(board):
        return None

    best_score = None
    maximizer = None
    best_action = None

    if player(board) == "X":
        maximizer = True
        best_score = -math.inf
    else:
        maximizer = False
        best_score = math.inf

    for action in actions(board):
        move = result(board, action)
        score = minimaxRec(move, not maximizer)
        
        if maximizer:
            if score > best_score:
                best_score = score
                best_action = action
        else:
            if score < best_score:
                best_score = score
                best_action = action

    return best_action

def minimax1(board):
    """Returns the optimal action for the current player on the board.
        """
    global X, O

    if terminal(board):
        return None


    best_score =  None # Least possible score
    maximizer = None
    best_score = -math.inf

    if player(board) == "X":
        best_score = -math.inf
        maximizer = True
    else:
        best_score = math.inf
        maximizer = False

    best_action = None
    print(maximizer)

    for action in actions(board):
        rslt = result(board, action)
        score = get_best_score(rslt, not maximizer)
        
        if maximizer:
            if score > best_score:
                best_score = score
                best_action = action
        else:
            if score < best_score:
                best_score = score
                best_action = action

    return best_action
