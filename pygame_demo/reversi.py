import random
import sys
import logging
# logging.basicConfig(level=logging.DEBUG)

def draw():
    x = "+-——+-——+-——+-——+-——+-——+-——+-——+"
    y = "|   |   |   |   |   |   |   |   |"
    print("1  2  3  4  5  6  7  8")
    print(x)
    for i in range(8):
        print(y)
        print(x)


def drawBoard(board):
    HLINE = " +------+------+------+------+------+------+------+------+"
    VLINE = " |      |      |      |      |      |      |      |      |"
    print(  "    1      2      3      4      5      6      7      8")
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end="")
        for x in range(8):
            if board[x][y] != "  ":
                print('| %s' % (board[x][y]), end="")
            else:
                print('|    %s'%(board[x][y]), end="")
        print("|")
        print(VLINE)
        print(HLINE)

def restBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = "  "
    board[3][3] = "  X  "
    board[3][4] = "  O  "
    board[4][3] = "  O  "
    board[4][4] = "  X  "

def getNewBoard():
    board = []
    for i in range(8):
        board.append(["  "] * 8)
    return board

def isOnBoard(x,y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != "  " or not isOnBoard(xstart,ystart):
        return False
    board[xstart][ystart] = tile
    if tile == "  X  ":
        otherTiie = "  O  "
    else:
        otherTiie = "  X  "

    tilesToFilp = []
    for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTiie:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTiie:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFilp.append([x, y])
    board[xstart][ystart] = "  "

    if len(tilesToFilp) == 0:
        return False
    return tilesToFilp


def getBoardCopy(board):
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x,y])
    return validMoves

def getBoardWithValidMoves(board,tile):
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '  *  '
    return dupeBoard

def getScoreOfBoard(board):
    score = {}
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == "  X  ":
                xscore += 1
            if board[x][y] == "  O  ":
                oscore += 1
    score = {"  X  ":xscore, "  O  ":oscore}
    return score

def enterPlayTile():
    playTile = []
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print("Do you want to be X or O?")
        tile = input().upper()

    if tile == 'O':
        playTile = ["  O  ", "  X  "]
    else:
        playTile = ["  X  ", "  O  "]

    return playTile

def whoGoesFirst():
    if random.randint(0,1) == 0:
        return "computer"
    else:
        return "player"

def playAgain():
    print("Do you want to play again? (yes or no)")
    return input().lower().startswith("y")

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
    DIGITS1To8 = "1 2 3 4 5 6 7 8".split()
    while True:
        print("Enter your move, or type quit to end the game, or hints to turn off/on hints.")
        move = input().lower()
        if move == 'quit':
            return "quit"
        if move == 'hints':
            return "hints"

        if len(move) == 2 and move[0] in DIGITS1To8 and move[1] in DIGITS1To8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print("That is not a valid move. Type the x digit(1-8), then y digit(1-8)")
            print("For example, 81 will be the top-right corner.")
    return [x, y]

def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board,computerTile)
    random.shuffle(possibleMoves)
    bestMove = []
    for x, y in possibleMoves:
        if isOnCorner(x,y):
            return [x][y]
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard,computerTile,x,y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def showPoints(board,playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print("You have %s points. The computer has %s points."%(scores[playerTile],scores[computerTile]))


while True:
    print("Welcome to Reversi!")
    mainBoard = getNewBoard()
    restBoard(mainBoard)
    playerTile, computerTile = enterPlayTile()
    showHints = False
    turn = whoGoesFirst()
    print("The %s will go first."%turn)

    while True:
        if turn == "player":
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(mainBoard, playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == "quit":
                print("Thank you playing!")
                sys.exit()
            elif move == "hints":
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])
            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = "computer"
        else:
            drawBoard(mainBoard)
            showPoints(mainBoard, playerTile, computerTile)
            input("Press Enter to see the computer's move.")
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)
            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = "player"

    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print("X scored %s points. O scored %s points."%(scores['  X  '],scores['  O  ']))
    if scores[playerTile] > scores[computerTile]:
        print("You beat the computer by %s points! Congratulation"%(scores[playerTile]-scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print("You lost! The computer beat you"%(scores[computerTile]-scores[playerTile]))
    else:
        print("The game was a tie!")

    if not playAgain():
        break