import time

# todo need to introduce 'y', for now the board is a square

board = []
sides = [0, 2, 1]
boardSize, line = 5, 3
# currPos strings reflect the positions and are used as a key in tt
currPos = "0" * (boardSize*boardSize)
tt = {}
colsOrdered = []
nodes = 0

'''
for an efficient minimax search, move ordering is important, here
it should check the moves starting from the cantral columns going towards
the edges so for example
for a range 0-4 it should be e.g. [2,1,3,0,4]
for a range 0-5 it should be e.g. [2,3,1,4,0,5]
'''


def setUpMoveOrdering():
    global colsOrdered

    col = -1
    if boardSize % 2 == 1:
        col = int(boardSize/2)
        colsOrdered.append(col)

        for i in range(1, int(boardSize/2)+1):
            colsOrdered.append(col+i)
            colsOrdered.append(col-i)

    else:
        col1 = int(boardSize/2) - 1
        col2 = int(boardSize/2)
        colsOrdered.append(col)

        for i in range(1, int(boardSize/2)):
            colsOrdered.append(col1-i)
            colsOrdered.append(col2+i)
    pass


'''
on the fly build a string that reflects the current
position. useful for debugging.
'''


def buildPositionString():
    global board
    s = ""
    for row in range(boardSize):
        for col in range(boardSize):
            s = s + str(board[row][col])
    return s
    pass


def printBoard():
    global board
    for row in board:
        for e in row:
            print (e, end=" ")
        print()
    pass


def genMoves():
    global board
    moves = []

    for col in range(boardSize):
        if board[0][col] == 0:

            row = 0
            while row < boardSize:
                if board[row][col] != 0:
                    break
                row += 1
            row -= 1

            moves.append([row, col])

    printBoard()
    print(moves)
    return moves
    pass


'''
look at the square [row,col], what color is on it (1,2 or 0), then check if
a line has been formed going through [row,col], made up of discs of this color
'''


def checkForLine(row, col):
    global board, line
    side = board[row][col]

    # horizontal
    x, y = 0, row
    aligned = 0
    while x < boardSize:
        if board[y][x] == side:
            aligned += 1
            if aligned >= line:
                return True
        else:
            aligned = 0
        x += 1

    # vertical
    x, y = col, 0
    aligned = 0
    while y < boardSize:
        if board[y][x] == side:
            aligned += 1
            if aligned >= line:
                return True
        else:
            aligned = 0
        y += 1

    # diagonals
    x, y = col, row
    while x+1 < boardSize and y+1 < boardSize:
        x += 1
        y += 1

    aligned = 0
    while x >= 0 and y >= 0:
        if board[y][x] == side:
            aligned += 1
            if aligned >= line:
                return True
        else:
            aligned = 0
        x -= 1
        y -= 1

    x, y = col, row
    while x+1 < boardSize and y > 0:
        x += 1
        y -= 1

    aligned = 0
    while x >= 0 and y < boardSize:
        if board[y][x] == side:
            aligned += 1
            if aligned >= line:
                return True
        else:
            aligned = 0
        x -= 1
        y += 1

    return False
    pass


def scanBoardForLine(side):
    global board
    for i in range(boardSize):
        for j in range(boardSize):
            if board[i][j] == side and checkForLine(i, j):
                return True

    return False
    pass


def miniMax(side, depth):
    global board, sides, currPos, nodes, colsOrdered

    nodes += 1

    sideOpp = sides[side]

    if currPos + str(side) in tt:
        return tt[currPos + str(side)]

    elif currPos + str(sideOpp) in tt:
        return -(tt[currPos + str(sideOpp)])

    moveMade = 0
    bestScore = -10000

    for col in colsOrdered:

        if board[0][col] == 0:
            moveMade = 1

            row = 0
            while row < boardSize:
                if board[row][col] != 0:
                    break
                row += 1
            row -= 1

            board[row][col] = side
            i = boardSize*row + col
            currPos = currPos[:i] + str(side) + currPos[i+1:]

            score = 0
            if checkForLine(row, col):
                score = 10000 - depth
            else:
                score = -miniMax(sideOpp, depth+1)

            board[row][col] = 0
            currPos = currPos[:i] + "0" + currPos[i+1:]

            if score > bestScore:
                bestScore = score

                if bestScore > 9000:
                    break

    if moveMade == 0:
        return 0

    ttPos = currPos + str(side)
    tt[ttPos] = bestScore

    assert (buildPositionString() == currPos)

    return bestScore
    pass


def miniMaxMain(side, depth):
    global board, sides, currPos, nodes, colsOrdered

    nodes += 1

    sideOpp = sides[side]

    moveMade = 0
    bestScore = -10000
    bestMove = [-1, -1]

    for col in colsOrdered:
        print('trying a move in main minimax')

        if board[0][col] == 0:
            moveMade = 1

            row = 0
            while row < boardSize:
                if board[row][col] != 0:
                    break
                row += 1
            row -= 1

            board[row][col] = side
            i = boardSize * row + col
            currPos = currPos[:i] + str(side) + currPos[i+1:]

            score = 0
            if checkForLine(row, col):
                score = 10000 - depth
            else:
                score = -miniMax(sideOpp, depth+1)

            board[row][col] = 0
            currPos = currPos[:i] + "0" + currPos[i+1:]

            if score > bestScore:
                bestScore = score
                bestMove = [row, col]

                # optimization, not perfect as might miss some faster wins
                if bestScore > 9000:
                    break

    print("max score is ", bestScore)

    if moveMade == 0:
        #print("game over. it's a draw.")
        pass

    return bestMove
    pass


def getMove():
    global board

    row = 0
    while True:
        col = input("enter a move. number to indicate the column  ")

        try:
            col = int(col)
        except ValueError:
            print("That's not an int!")
            continue

        # make sure its in the interval 0 - boardSize-1
        if col < 0 or col >= boardSize:
            print("really need to enter number between 0 and ", boardSize-1)
            continue

        # if the column all filled, prompt again
        if board[0][col] != 0:
            print("looks like this column is filled")
            continue

        while row < boardSize:
            if board[row][col] != 0:
                break
            row += 1
        row -= 1
        break

    return [row, col]
    pass


def playConnect4():
    global board, sides, currPos, nodes

    setUpMoveOrdering()

    humSide, compSide = 1, 2
    sideToPlay = 2

    while True:

        try:
            sideToPlay = int(input("pick who starts. 1 - human, 2 - computer"))
        except ValueError:
            print("not an int!")
            continue

        if sideToPlay == 1 or sideToPlay == 2:
            break
        else:
            print("not a correct value!")

    while True:
        print("--------------------------------")

        if sideToPlay == humSide:
            mv = getMove()
            board[mv[0]][mv[1]] = humSide

            i = boardSize*(mv[0]) + mv[1]
            currPos = currPos[: i] + str(humSide) + currPos[i+1:]

        else:

            start = time.time()
            nodes = 0

            mv = miniMaxMain(compSide, 0)
            board[mv[0]][mv[1]] = compSide

            i = boardSize*(mv[0]) + mv[1]
            currPos = currPos[:i] + str(compSide) + currPos[i+1:]

            end = time.time()
            print("time elapsed ", end - start)
            print("nm of nodes", nodes)

        printBoard()

        if scanBoardForLine(sideToPlay):
            break

        sideToPlay = sides[sideToPlay]

    pass


board = [[0]*boardSize for _ in range(boardSize)]
playConnect4()



'''
testing checkForLine on a 5x5 board

'''


def mytest(pos, coords, rets):

    for i in range(len(pos)):
        for j in range(len(pos[0])):
            board[i][j] = int(pos[i][j])

    for i in range(len(coords)):
        assert(checkForLine(coords[i][0], coords[i][1]) == rets[i])

    pass


newpos = ['10000', '01000', '00100', '00020', '11121']
coords = [[4, 1], [4, 3], [0, 0], [1, 1], [2, 2], [3, 3]]
rets = [True, False, True, True, True, False]

#mytest(newpos, coords, rets)

newpos = ['11221', '22112', '11221', '22112', '11221']
coords = [[j, i] for j in range(5) for i in range(5)]
rets = (5*5) * [False]

#mytest(newpos, coords, rets)

