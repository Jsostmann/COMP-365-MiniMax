"""Tic Tac Toe implementation"""
import copy
import math

X = "X"
O = "O"
EMPTY = None

'''Returns starting state of the board.'''
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


'''Returns player who has the next turn on a board.'''
def player(board):
    
    # bring in global X and O player values
    global X, O
    
    # declare values to hold count of X player and O player on board
    xCount = 0
    oCount = 0
    
    for row in board:
        for col in row:
            if col == X:
                xCount += 1
            elif col == O:
                oCount += 1

    # check if there is more X moves than O, if there is next player is O otherwise always X first
    if oCount < xCount:
        return O

    return X


'''Returns set of all possible actions (i, j) available on the board.'''
def actions(board):
    # set to hold our actions
    allActions = set()
    
    # loop through all rows in board with rowIndex
    for rowIndex, row in enumerate(board):
        # loop through all collumns in row with index colIndex
        for colIndex, col in enumerate(row):
            # if the space at board[rowIndex][colIndex] is free create and add a tuple containing (rowIndex, colIndex) to allActions
            if col is None:
                #indexTuple = (rowIndex, colIndex)
                allActions.add((rowIndex, colIndex))

    return allActions

'''Returns the board that results from making move (i, j) on the board.'''
def result(board, action):
    
    global EMPTY
    
    # allocate new memory for a copy of the board
    boardCopy = copy.deepcopy(board)
    
    # get the values from the action tuple
#rowIndex = action[0]
#    colIndex = action[1]
    rowIndex , colIndex = action

    if boardCopy[rowIndex][colIndex] is EMPTY:
        boardCopy[rowIndex][colIndex] = player(board)

    return boardCopy


'''returns True if there are moves left, False if there isnt'''
def movesLeft(board):
    
    # bring in global Empty values
    global EMPTY

    for row in board:
        for col in row:
            if col is EMPTY:
                return True
    return False

'''Returns the winner of the game, if there is one.'''
def winner(board):
    
    win = None
    
    # checks for diagonal winner from top left to bottom right and bottom left to top right
    if(board[1][1] == board[0][0] and board[0][0] == board[2][2])\
        or (board[1][1] == board[0][2] and board[0][2] == board[2][0]):
            win = board[1][1]
            return win

    for i in range(3):
        #checks for winner on each row
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            win = board[i][1]
            break
        
        # checks for winner on each collumn
        elif board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            win = board[1][i]
            break

    return win

'''Returns True if game is over, False otherwise.'''
def terminal(board):
    if winner(board) is None and movesLeft(board):
        return False
    return True;


'''Returns 1 if X has won the game, -1 if O has won, 0 otherwise.'''
def utility(board):
    
    # bring in global X and O player values
    global X, O

    if terminal(board):
        gameWinner = winner(board)

        if gameWinner == X:
            winnerNumber = 1
        
        elif gameWinner == O:
            winnerNumber = -1

        else:
            winnerNumber = 0

        return winnerNumber
            
    return None


'''our helper recursive method for the minimax function'''
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

'''Returns the optimal action for the current player on the board.'''
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
        move = result(board,action)
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
