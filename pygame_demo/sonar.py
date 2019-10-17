import random
import sys
import math

# 本质是对二维列表的操作

def getNewBoard():
    board = []
    for x in range(60):
        board.append([])
        for y in range(15):
            if random.randint(0,1) == 0:
                board[x].append('~')
            else:
                board[x].append("`")
    return board

def drawBoard(board):
    tensDigitsLine = " "
    for i in range(1,6):
        tensDigitsLine += (" "*9)+str(i)
    print(tensDigitsLine)
    print("   "+"0123456789"*6)
    print()

    for row in range(15):
        if row < 10:
            extraSpace = "  "
        else:
            extraSpace = " "
        boardRow = ""
        for column in range(60):
            # 二维列表
            boardRow += board[column][row]
        print("%s%s %s %s "% (extraSpace, row, boardRow, row))
    print()
    print("   " + "0123456789" * 6)
    print(tensDigitsLine)

def getRandomChests(numChests):
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0,59),random.randint(0,14)]
        if newChest not in chests:
            chests.append(newChest)
    return chests

def isOnBoard(x, y):
    return x >= 0 and x <= 59 and y >= 0 and y <= 14

def makeMove(board, chests, x, y):
    smailDistance = 100
    for cx, cy in chests:
        distance = math.sqrt((cx-x)*(cx-x)+(cy-y)*(cy-y))

        if distance < smailDistance:
            smailDistance = distance
    smailDistance = round(smailDistance)

    if smailDistance == 0:
        chests.remove([x,y])
        return "You have found a sunken treasure chest"
    else:
        if smailDistance < 10:
            board[x][y] = str(smailDistance)
            return "Treasure detected at distance of %s from the sonar device"%(smailDistance)
        else:
            board[x][y] = 'X'
            return "Sonar did not detect anything. All treasure chests out of range"

def enterPlayerMove(previousMove):
    print("Where do you want to drop the next sonar device?(0-59,0-14)")
    # print("Where do you want to drop the next sonar device?(0-59 0-14) or type quit")
    while True:
        move = input()
        if move.lower() == 'quit':
            print("Thinks for playing!")
            sys.exit()
        move = move.split(",")
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
            if[int(move[0]), int(move[1])] in previousMove:
                print("You are already moved there.")
                continue
            return [int(move[0]), int(move[1])]
        print("Enter a number from 0 to 59,a space, than a number from 0 to 14")

def playAgain():
    print("Do you want to play again ? (yes or no)")
    return input().lower().startswith("y")

def showInstructions():
    print("Press enter to continue")
    input()
    print("S O N A R!")
    print()
    print('Would you like to view the instructions? (yes or no)')
    if input().lower().startswith("y"):
        showInstructions()

while True:
    sonarDevices = 2
    theBoard = getNewBoard()
    theChests = getRandomChests(3)
    drawBoard(theBoard)
    previousMove = []

    while sonarDevices > 0:
        print("You have %s sonar device(s) left. %s treasure chest(s) remaining."%(sonarDevices,len(theChests)))
        x,y = enterPlayerMove(previousMove)
        previousMove.append([x,y])
        moveResult = makeMove(theBoard,theChests,x,y)
        if moveResult == False:
            continue
        else:
            if moveResult == "You have found a sunken treasure chest":
                for x, y in previousMove:
                    makeMove(theBoard, theBoard, x, y)
            drawBoard(theBoard)
            print(moveResult)

        if len(theChests) == 0:
            print("You have found all the sunken treasure chest(s)! Congratulation and good game!")
            break

        sonarDevices -= 1

        if sonarDevices == 0:
            print("Game Over")
            print("The remaining chests were here:")
            for x, y in theChests:
                print("%s, %s" % (x, y))
                theBoard[x][y] = "O"
            drawBoard(theBoard)

            if not playAgain():
                sys.exit()
