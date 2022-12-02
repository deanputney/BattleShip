import math, copy, random
import time
from cmu_112_graphics import *


# ship class and different ship types
class ship():
    def __init__(self, app, shipCoord, outline, shipType):
        self.shipCoord = shipCoord #actual coords of the ship
        self.outline = outline #outline which other ships cant enter
        self.app = app
        self.shipType = shipType

    def getCoordinates(self):
        return self.shipCoord
    
    def getShipType(self):
        return self.shipType

    def moveShip(self, drow, dcol):
        oldCoord = copy.deepcopy(self.shipCoord)
        oldOutline = copy.deepcopy(self.outline)
        
        # creates temp ship to test
        newCoord = []
        for coord in self.shipCoord:
            row, col = coord

            newRow = row + drow
            newCol = col + dcol

            newCoord.append((newRow, newCol))
            
        removeOldOutline(self.app, oldOutline)
        removeOldCoords(self.app, oldCoord)
        addOtherOutlines(self.app)

        newOutline = getOutline(self.app, newCoord)
        if newOutline == False:
            print("outline false")
            self.shipCoord = oldCoord
            self.outline = oldOutline
        else:
            # tests if new coords are legal
            if isShipLegal(self.app, newCoord, newOutline) == False:
                print("ship not legal = didnt move")
                self.shipCoord = oldCoord
                self.outline = oldOutline
                addOutline(self.app, oldOutline)
            elif isShipLegal(self.app, newCoord, newOutline):
                print("moved")
                removeOldCoords(self.app, oldCoord)
                removeOldOutline(self.app, oldOutline)
                addOutline(self.app, newOutline)
                addCoords(self.app, newCoord, self.shipType)
                self.shipCoord = newCoord
                self.outline = newOutline
        
        print(f"moveship coords{self.shipCoord}")
        print(f"updated board = {self.app.turn.boardShips}")
    
    def draw(self):
        pass


# FIX ROTATED
    def rotate(self, app):
        oldCoord = copy.deepcopy(self.shipCoord)
        oldRowLenCoord = len(self.shipCoord)
        oldColLenCoord = len(self.shipCoord[0])

        oldOutline = copy.deepcopy(self.outline)
        oldRowLenOutline= len(self.outline)
        oldColLenOutline= len(self.outline[0])

        newRowLenCoord = oldColLenCoord
        newColLenCoord = oldRowLenCoord

        newRowLenOutline = oldColLenOutline
        newColLenOutline = oldRowLenOutline

        rotatedShip = []
        for i in range(oldColLenCoord):
            tempRow = []
            for j in range(oldRowLenCoord):
                tempRow.append(None)
            rotatedShip.append(tempRow)

        for i in range(0, oldRowLenCoord):
            for j in range(oldColLenCoord-1, -1, -1):
                temp = oldCoord[i][j]
                rotatedShip[oldColLenCoord-j-1][i] = temp

        self.shipCoord = copy.deepcopy(rotatedShip)

        # # centering
        # newRow = app.fallingPieceRow + oldRowLen//2 - newRowLen//2
        # newCol = app.fallingPieceCol + oldColLen//2 - newColLen//2

        # app.fallingPieceRow = newRow
        # app.fallingPieceCol = newCol

        # if fallingPieceIsLegal(app) == False:
        #     app.fallingPiece = oldPiece
        #     app.fallingPieceRow = oldRow
        #     app.fallingPieceCol = oldCol
# ==============

        # oldPiece = copy.deepcopy(app.fallingPiece)
        # oldRowLen = len(app.fallingPiece)
        # oldColLen = len(app.fallingPiece[0])

        # newRowLen = oldColLen
        # newColLen = oldRowLen

        # oldRow = app.fallingPieceRow
        # oldCol = app.fallingPieceCol

        # rotatedPiece = []
        # for i in range(oldColLen):
        #     tempRow = []
        #     for j in range(oldRowLen):
        #         tempRow.append(None)
        #     rotatedPiece.append(tempRow)

        # for i in range(0, oldRowLen):
        #     for j in range(oldColLen-1, -1, -1):
        #         temp = oldPiece[i][j]
        #         rotatedPiece[oldColLen-j-1][i] = temp

        # app.fallingPiece = copy.deepcopy(rotatedPiece)
        
        # # centering
        # newRow = app.fallingPieceRow + oldRowLen//2 - newRowLen//2
        # newCol = app.fallingPieceCol + oldColLen//2 - newColLen//2

        # app.fallingPieceRow = newRow
        # app.fallingPieceCol = newCol

        # if fallingPieceIsLegal(app) == False:
        #     app.fallingPiece = oldPiece
        #     app.fallingPieceRow = oldRow
        #     app.fallingPieceCol = oldCol

def removeOldOutline(app, outline):
    for coord in outline:
        rowCoord, colCoord = coord
        app.turn.boardShips[rowCoord][colCoord] = -1

def addOutline(app, outline):
    for coord in outline:
        rowCoord, colCoord = coord
        app.turn.boardShips[rowCoord][colCoord] = 0

def removeOldCoords(app, oldCoord):
    for coord in oldCoord:
        rowCoord, colCoord = coord
        app.turn.boardShips[rowCoord][colCoord] = -1

def addCoords(app, coords, shipType):
    for coord in coords:
        rowCoord, colCoord = coord
        app.turn.boardShips[rowCoord][colCoord] = shipType
    
def addOtherOutlines(app):
    for ship in app.turn.ships:
        if ship == app.selectedShip:
            continue
        else:
            coords = ship.getCoordinates()
            outline = getOutline(app, coords)
            addOutline(app, outline)



# have drawing function for ship class --> ship.draw
# home grown algorithm
# monte carlo: most likey to put where --> learn to put in certain places
# 1. be able to play with two players
# 2. set up AI class (rand) 
# 3. 3rd AI should do something smarter --> find patterns in what people play
# look at expecamax (likely to do this, so i chose something to do that will make me max my score)
# level/board generation --> make backtracker to make a board that can fit the different ships

# draw directly on screen --> draw what your trying to print in canvas
# have two board for two players --> screen switches when player switches (call board1, or board2 --> depends on player)
# model view controler so don need more than 2 boards

class smallShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): #shipcoord and outline will be sent from create ships
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()    

class medShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()

class bigShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()

class lShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()
    
class oShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()

class uShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()

class tShip(ship):
    def __init__(self, app, shipCoord, outline, shipType): 
        super().__init__(app, shipCoord, outline, shipType)
        super().getCoordinates()
        super().draw()
        super().getShipType()

class player():
    def __init__(self, app, id, boardRows, boardCols, emptyColor, allShips):
        self.app = app
        self.rows = boardRows
        self.cols = boardCols
        self.id = id
        self.destroyedShips = 0

        self.board = []
        for i in range(self.rows):
            newRow = []
            for j in range(self.cols):
                newRow.append(emptyColor)
            self.board.append(newRow)

        self.boardShips = []
        for i in range(self.rows):
            newRow = []
            for j in range(self.cols):
                newRow.append(-1)
            self.boardShips.append(newRow)

        # the places you chose to hit
        self.boardHits = []
        for i in range(self.rows):
            newRow = []
            for j in range(self.cols):
                newRow.append(-1)
            self.boardHits.append(newRow)

        self.allShips = allShips
        self.ships = []
        self.allMoves = []
        self.previousSuccess = []
    
    def getId(self):
        return self.id
    def board(self):
        return self.board
    def boardShips(self):
        return self.boardShips
    def boardHits(self):
        return self.boardHits
    def ships(self):
        return self.ships
    def getMoves(self):
        self.allMoves = []
        for row in range(self.app.rows):
            for col in range(self.app.cols):
                if self.boardHits[row][col] == -1:
                    self.allMoves.append((row, col))
        
        return self.allMoves
    
    def shipDestroyed(self):
        self.destroyedShips += 1
    def destroyedShips(self):
        return self.destroyedShips
    def getPreviousSuccess(self):
        return self.previousSuccess

# model and view functions
# -----------------------------------------------------------------------------------------------
# from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

# Used for grid 1
def pointInGrid1(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.cols*app.cellSize+app.margin) and
            (app.margin*(5/2) <= y <= app.rows*app.cellSize+app.margin*(5/2)))

def getCell1(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid1(app, x, y)):
        # print("not in grid")
        return (-1, -1)
    # print("ingrid")
    gridWidth  = app.cols*app.cellSize
    gridHeight = app.rows*app.cellSize
    cellWidth  = app.cellSize
    cellHeight = app.cellSize

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin*(5/2)) // cellHeight)
    col = int((x - app.margin) // cellWidth)

    return (row, col)

#used for grid 2
def pointInGrid2(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin*2 + app.cols*app.cellSize <= x <= app.margin*2 + app.cols*app.cellSize + app.cols*app.cellSize) and
            (app.margin*(5/2) <= y <= app.rows*app.cellSize+app.margin*(5/2)))

def getCell2(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid2(app, x, y)):
        # print("not in grid")
        return (-1, -1)
    # print("ingrid")
    gridWidth  = app.cols*app.cellSize
    gridHeight = app.rows*app.cellSize
    cellWidth  = app.cellSize
    cellHeight = app.cellSize

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin*(5/2)) // cellHeight)
    col = int((x - app.margin*2 - app.cols*app.cellSize) // cellWidth)

    return (row, col)

def getCellBounds2(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.cols*app.cellSize
    gridHeight = app.rows*app.cellSize
    cellWidth  = app.cellSize
    cellHeight = app.cellSize
    x0 = app.margin*2 + app.cols*app.cellSize + col * cellWidth
    x1 = app.margin*2 + app.cols*app.cellSize + (col+1) * cellWidth
    y0 = app.margin*(5/2) + row * cellHeight
    y1 = app.margin*(5/2) + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# interactive functions (pressed) and helper functions
# -----------------------------------------------------------------------------------------------

def keyPressed(app, event):
    # print("keypressed")

    if app.setup == True:
        ship = app.selectedShip
        # print(f"key pressed ship = {ship}")
        if ship != None:
            if event.key == "Up":
                ship.moveShip(-1, 0)
            if event.key == "Down":
                ship.moveShip(1, 0)
            if event.key == "Left":
                ship.moveShip(0, -1)
            if event.key == "Right":
                ship.moveShip(0, 1)

            if event.key == "Space":
                ship.rotate(app)

def mousePressed(app, event):   # use event.x and event.y
    print("mousepressed")
    # all mousePressed for homepage
    if app.homepage == True:
        # multiplayer button
        if (event.x >= app.width*(2/7) and 
            event.x <= app.width*(5/7) and
            event.y >= app.height*(1/4) + app.height*(1/6) + + app.height*(1/20) and
            event.y <= app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/20)):
            app.multiplayer = True
            app.homepage = False
            app.setup = True
            
        # practice button
        elif (event.x >= app.width*(2/7) and 
            event.x <= app.width*(5/7) and
            event.y >= app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + app.height*(1/10) and
            event.y <= app.height*(1/4) + app.height*(1/6) + app.height*(2/7) + app.height*(1/10)):
            app.practice = True
            app.homepage = False
            app.settings = True

    # All mouse pressed for settings
    elif app.settings == True:
        # easy button
        if (event.x >= app.width*(1/9) - app.width*(1/18) and 
                event.x <= app.width*(3/9) - app.width*(1/18) and
                event.y >= app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) and
                event.y <= app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10)):
                app.settings = False
                app.difficulty = "easy"
                app.setup = True
                app.ai = randomA(app)

        # medium button
        if (event.x >= app.width*(4/9) - app.width*(1/18) and 
                event.x <= app.width*(6/9) - app.width*(1/18) and
                event.y >= app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) and
                event.y <= app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10)):
                app.settings = False
                app.difficulty = "medium"
                app.setup = True
                app.ai = huntA(app)

        # hard button
        if (event.x >= app.width*(7/9) - app.width*(1/18) and 
                event.x <= app.width*(9/9) - app.width*(1/18) and
                event.y >= app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) and
                event.y <= app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10)):
                app.settings = False
                app.difficulty = "hard"
                app.setup = True

    # all mousePressed for setup page
    elif app.setup == True:
        # select ship
        (row, col) = getCell1(app, event.x, event.y)
        app.selection = (row, col)
        print(f"mousepressed row col = {row, col}")
        checkWhichShip(app)

        # finish setup button 
        if (event.x >= app.margin*2 + app.cols*app.cellSize and 
            event.x <= app.margin*2 + app.cellSize*5 + app.cols*app.cellSize and
            event.y >= app.margin*(5/2) + app.rows*app.cellSize - 50 and
            event.y <= app.margin*(5/2) + app.rows*app.cellSize):
            
            # finish setup page for player 1
            if app.turn.getId() == 1:
                app.setup = True
                app.gameStarted = False
                app.turn = app.player2
            # finish setup page for player 2
            elif app.turn.getId() == 2:
                app.selection = (-1, -1)
                app.turn = app.player1
                app.setup = False
                app.gameStarted = True

    # all mousePressed for gameplay
    elif app.gameStarted == True:

        if app.multiplayer == True:
            # checks if a box was selected in the grid and which box
            (row, col) = getCell2(app, event.x, event.y)
            if app.turn.boardHits[row][col] < 0:
                app.selection = (row, col)
                # print(f"coords from select = {app.selection}")
                # print(f"mousepressed row col = {row, col}")
                
                makeHit(app, app.selection)
                # checks if a ship was hit
                if checkHit(app, app.selection) == True:
                    # checks if all ship parts bombed, if true calls completedShip
                    shipAllBombed(app, app.selection)
                
                # if a move was made, the player will switch
                elif app.selection != (-1, -1):
                    if app.turn.getId() == 1:
                        app.turn = app.player2
                    elif app.turn.getId() == 2:
                        app.turn = app.player1
        
        elif app.practice == True:
            if app.turn.getId() == 1:
                (row, col) = getCell2(app, event.x, event.y)
                if app.turn.boardHits[row][col] < 0:
                    app.selection = (row, col)
                    # print(f"coords from select = {app.selection}")
                    # print(f"mousepressed row col = {row, col}")
                    
                    makeHit(app, app.selection)
                    # checks if a ship was hit
                    if checkHit(app, app.selection) == True:
                        # checks if all ship parts bombed, if true calls completedShip
                        shipAllBombed(app, app.selection)
                    
                    # if a move was made, the player will switch
                    elif app.selection != (-1, -1):
                        checkWin(app)

                        if app.turn.getId() == 1:
                            print("in pressed p1")
                            print(f"turn = {app.turn.getId()}")
                            app.turn = app.player2
                            # runAI(app)
                            app.ai.makeMove()
                            if app.player2.getPreviousSuccess() != []:
                                app.ai.makeMove()
                            # app.turn = app.player1

                        # elif app.turn.id == 2:
                        #     app.turn = app.player1
            if app.turn.getId() == 2:
                app.ai.makeMove()

                
def runAI(app):
    pass
    # print(f"turn = {app.turn.id}")
    # if app.practice == True:
    #     print("--------")
    #     print("AI started")
    #     if app.turn.id == 2:
    #         print("correct")
    #         if app.difficulty == "easy":
    #             randomAI(app)

    #         elif app.difficulty == "medium":
    #             print("correct2")
    #             print(f"checkhit = {checkHit(app)}")
    #             print(f"prev = {app.player2.previousSuccess}")
    #             print("---------------")

    #             if checkHit(app) == False and app.player2.previousSuccess == -1:
    #                 print("going to RAND")
    #                 print(f"checkhit rand = {checkHit(app)}")
    #                 print(f"prev rand = {app.player2.previousSuccess}")
    #                 # randomAI(app)
    #                 checkWin(app)
    #                 app.turn = app.player1

    #             elif app.player2.previousSuccess != -1:
    #                 print("going to HUNT")
    #                 print(f"checkhit hunt = {checkHit(app)}")
    #                 print(f"prev hunt = {app.player2.previousSuccess}")
    #                 huntAI(app)
    #                 checkWin(app)
    #                 app.turn = app.player1

    #         elif app.difficulty == "hard":
    #             pass
        
    #     print(f"turn = {app.turn.id}")
        
# look at wordsearch
# seperate two ais into diff classes --> AI = instace of AI
# ai.make decision
# /////////////////////////////////////////////////////////////////////////////////////
# class huntA():
#     def __init__(self, app):
#         self.app = app
#         self.directions = [(0,-1), (-1,0), (0,1), (1,0)]
        
#         # self.directions = [(-1, -1), (0, -1), (1, -1), 
#         #                     (-1, 0), (1, 0), 
#         #                     (-1, 1), (0, 1), (1, 1)]
#         self.hit = None
        
#     def randomMove(self):
#         while True:
#             print("---")
#             print("in rand move")
#             print(f"turn = {self.app.turn.getId()}")
#             randRow = random.randint(0, self.app.rows-1)
#             randCol = random.randint(0, self.app.cols-1)

#             print(f"random coord = {randRow, randCol}")
            
#             self.hit = (randRow, randCol)

#             possibleMoves = self.app.player2.getMoves()

#             if (randRow, randCol) in possibleMoves:
#                 makeHit(self.app, self.hit)
#                 if checkHit(self.app, self.hit) == False:
#                     print(f"unsuccess hit rand = {self.hit}")
#                     self.app.player2.previousSuccess = []
#                     self.app.turn = self.app.player1
#                     break

#                 elif checkHit(self.app, self.hit) == True:
#                     print(f"success hit rand = {self.hit}")
#                     self.app.player2.previousSuccess.append(self.hit)

#                 if shipAllBombed(self.app, self.hit) == True:
#                     print("__all bombed__1")
#                     self.app.player2.previousSuccess = []
        
#             if self.app.player2.getPreviousSuccess() != []:
#                 break
    
#     def huntMove(self):
#         while True:
#             print("---")
#             print("in hunt move")
#             print(f"turn = {self.app.turn.getId()}")
#             print(self.app.player2.getPreviousSuccess())
            
#             prevSuccesses = self.app.player2.getPreviousSuccess()
#             hitMade = False
#             print(f"prev successes = {prevSuccesses}")
#             while hitMade == False:
#                 for prevSucc in prevSuccesses:
#                 # while self.app.player2.getPreviousSuccess() != []: #or should i do for loop going though all of prevSucc and pop each elem that doesnt work?
#                     # prevSucc = self.app.player2.getPreviousSuccess()
#                     print(f"prevSucc = {prevSucc}")
#                     row, col = prevSucc
                    
#                     counter = 0
#                     for d in self.directions:
#                         counter += 1
#                         print(f"direction = {d}")
#                         drow, dcol = d
#                         newRow = row + drow
#                         newCol = col + dcol

#                         newHit = (newRow, newCol)

#                         possibleMoves = self.app.player2.getMoves()
#                         if newHit in possibleMoves:
#                             print("hit possible")
#                             self.hit = newHit
#                             makeHit(self.app, self.hit)
#                             break
#                             print("continue?")

#                         if counter == 4:
#                             print("popped")
#                             self.app.player2.previousSuccess.pop(0)
#                     print("still in loop")
#                     hitMade = True

#             if checkHit(self.app, self.hit) == False:
#                     print(f"unsuccess hit hunt = {self.hit}")
#                     # self.app.player2.previousSuccess = -1
#                     self.app.turn = self.app.player1
#                     break

#             elif checkHit(self.app, self.hit) == True:
#                 print(f"success hit hunt = {self.hit}")
#                 self.app.player2.previousSuccess.append(self.hit)

#                 if shipAllBombed(self.app, prevSuccesses[0]) == True:
#                     print("__all bombed__2")
#                     self.app.player2.previousSuccess = []

#             if self.app.player2.getPreviousSuccess() != []:
#                 print("enter ???")
#                 break

#     def makeMove(self):
#         if self.app.turn.getId() == 2:
#             print(f"make move player = {self.app.turn.getId()}")
#             if self.app.player2.getPreviousSuccess() == []:
#                 print("gg in rand move")
#                 self.randomMove()
#             else:
#                 print("gg in hunt move")
#                 print(f"prev succ = {self.app.player2.getPreviousSuccess()}")
#                 self.huntMove()
# /////////////////////////////////////////////////////////////////////////////////////
class huntA():
    def __init__(self, app):
        self.app = app
        self.directions = [(0,-1), (-1,0), (0,1), (1,0)]
        self.hit = None
        
    def possibleMove(self, row, col):
        possibleMoves = self.app.player2.getMoves()
        if (row, col) in possibleMoves:
            return True
        
    def makeMove(self):
        while self.app.turn.getId() == 2:
            # print(f"make move player = {self.app.turn.getId()}")
            print("------------------------------------------finish function")
            if self.app.player2.getPreviousSuccess() == []:
                print("gg in rand move")
                print(f"prev succ = {self.app.player2.getPreviousSuccess()}")
                self.randomMove()
            else:
                print("gg in hunt move")
                print(f"prev succ = {self.app.player2.getPreviousSuccess()}")
                self.huntMove()
        print("while loop exited")
        
    def huntMove(self):
        print("------------------------------------------")
        print("in hunt")
        print("---")
        prevSuccesses = self.app.player2.getPreviousSuccess()
        mostRecentSucc = prevSuccesses[-1]

        counter = 0
        for d in self.directions:
            drow, dcol = d
            row, col = mostRecentSucc
            newRow, newCol = row + drow, col + dcol

            if self.possibleMove(newRow, newCol) == False:
                counter += 1
                if counter == 4:
                    prevSuccesses.pop(-1)
                    print("popped")

            elif self.possibleMove(newRow, newCol) == True:
                print(f"HUNT: possible move is true = {newRow, newCol}")
                self.hit = (newRow, newCol)
                makeHit(self.app, self.hit)

                if checkHit(self.app, self.hit) == False:
                    print(f"unsuccess hit rand = {self.hit}")
                    # self.app.player2.previousSuccess = []
                    self.app.turn = self.app.player1
                    print("HUNT: prev succ cleared - checkHit")
                    print(self.app.turn.getId())
                    break

                elif checkHit(self.app, self.hit) == True:
                    self.app.player2.previousSuccess.append(self.hit)

                if shipAllBombed(self.app, self.hit) == True:
                    print("__all bombed__1")
                    self.app.player2.previousSuccess = []
                    print("HUNT: prev succ cleared - allbombed")
                
    def randomMove(self):
            print("------------------------------------------")
            print("in rand")
        # while True:
            print("---")
            print(f"turn = {self.app.turn.getId()}")
            randRow = random.randint(0, self.app.rows-1)
            randCol = random.randint(0, self.app.cols-1)

            print(f"random coord = {randRow, randCol}")
            
            self.hit = (randRow, randCol)

            if self.possibleMove(randRow, randCol) == True:
                print(f"RAND: possible move is true = {randRow, randCol}")
                makeHit(self.app, self.hit)

                if checkHit(self.app, self.hit) == False:
                    print(f"unsuccess hit rand = {self.hit}")
                    # self.app.player2.previousSuccess = []
                    self.app.turn = self.app.player1
                    print("RAND: prev succ cleared - checkHit")
                    # break

                elif checkHit(self.app, self.hit) == True:
                    print(f"success hit rand = {self.hit}")
                    self.app.player2.previousSuccess.append(self.hit)

                elif shipAllBombed(self.app, self.hit) == True:
                    print("__all bombed__1")
                    self.app.player2.previousSuccess = []
                    print("RAND: prev succ cleared - allbombed")
        
            # if self.app.player2.getPreviousSuccess() != []:
            #     break



def huntAI(app):
    pass
#     print("entered HUNT")
#     while True:
#         directions = [(-1, -1), (0, -1), (1, -1), 
#                         (-1, 0), (1, 0), 
#                         (-1, 1), (0, 1), (1, 1)]
#         possibleMoves = app.player2.getMoves()
#         print(possibleMoves)
#         # if checkHit(app) == False:
#         #     randomAI(app)

#         if checkHit(app) == True:
            
#             (row, col) = app.player2.previousSuccess()
#             for d in directions:
#                 drow = d[0]
#                 dcol = d[1]
#                 newRow = row + drow
#                 newCol = col + dcol
#                 if (newRow, newCol) in possibleMoves:
#                     print("move made")
#                     makeHit(app)
#                     if checkHit(app) == True:
#                         shipAllBombed(app)
#                         break

#         if shipAllBombed(app) == True:
#             app.player2.previousSuccess = -1
#         # checkWin(app)
#         # app.turn = app.player1
#         break

class randomA():
    def __init__(self, app):
        self.app = app
    def makeMove(self):
        while True:
            randRow = random.randint(0, self.app.rows-1)
            randCol = random.randint(0, self.app.cols-1)

            print(f"random coord = {randRow, randCol}")
            
            hit = (randRow, randCol)

            possibleMoves = self.app.player2.getMoves()

            if (randRow, randCol) in possibleMoves:
                makeHit(self.app, hit)
                if checkHit(self.app, hit) == False:
                    print("unsuccess hit")
                    self.app.player2.previousSuccess = []
                    self.app.turn = self.app.player1

                elif checkHit(self.app, hit) == True:
                    print("success hit")
                    self.app.player2.previousSuccess.append(hit)

                if shipAllBombed(self.app, hit) == True:
                    print("__all bombed__")
                    self.app.player2.previousSuccess = []
            break


def randomAI(app):
    pass
#     print("entered RAND")
#     while True:
#         # randomizes a row and col for the hit
#         randRow = random.randint(0, app.rows-1)
#         randCol = random.randint(0, app.cols-1)
#         # saves possible moves

#         possibleMoves = app.player2.getMoves()

#         # checks if the row and col are valid moves (have not been selected before)
#         if (randRow, randCol) in possibleMoves:
#             # print("move made")
#             # app.selection = (randRow, randCol)
#             makeHit(app)
#             # checks if the randomized move hit a ship
#             if checkHit(app) == False:
#                 print("unsuccess hit")
#                 app.player2.previousSuccess = -1
#             elif checkHit(app) == True:
#                 print("success hit")
#                 # keeps track of the previous successful hit if the whole ship is not bombed
#                 app.player2.previousSuccess = app.selection
#                 # checks if all ship parts bombed, if true calls completedShip
#                 if shipAllBombed(app) == True:
#                     print("__all bombed__")
#                     app.player2.previousSuccess = -1

#         # swaps players
#         # checkWin(app)
#         # app.turn = app.player1
#         break
            
# checks which ship was selected (setup page)
def checkWhichShip(app):
    # playerShips = None
    playerShips = app.turn.ships
    for ship in playerShips:
        # print("newSHIP")
        coords = ship.getCoordinates()
        # print(f"ship coords{coords}, slected = {app.selection}")
        if app.selection in coords:
            app.selectedShip = ship
            break
    return None
        
# checks if a ship was hit and for which player (gameplay)
def checkHit(app, hit):
    # print("check Hit")
    # print(f"app.sele = {app.selection}")
    if app.gameStarted == True:
        if hit != (-1, -1):
            row, col = hit
            if app.turn.getId() == 1:
                # checks if ship was hit
                print(f"player 1 hit = {app.player2.boardShips[row][col]}")
                if app.player2.boardShips[row][col] > 0:
                    return True
                # if ship wasn't hit
                else:
                    return False
            if app.turn.getId() == 2:
                print(f"player 2 hit = {app.player1.boardShips[row][col]}")
                if app.player1.boardShips[row][col] > 0:
                    return True
                else:
                    return False
                
def makeHit(app, hit):
    print("##########")
    if app.gameStarted == True:
        if hit != (-1, -1):
            row, col = hit
            if app.turn.getId() == 1:
                print("making hit for 1")
                # checks if ship was hit
                if app.player2.boardShips[row][col] > 0:
                    app.turn.boardHits[row][col] = 2
                # if ship wasn't hit
                else:
                    app.turn.boardHits[row][col] = 1
            if app.turn.getId() == 2:
                print("making hit for 2")
                if app.player1.boardShips[row][col] > 0:
                    app.turn.boardHits[row][col] = 2
                else:
                    app.turn.boardHits[row][col] = 1

# checks if all parts of ship are bombed (gameplay)
def shipAllBombed(app, hit):
    if app.turn.getId() == 1:
        playerShips = app.player2.ships
        # checks if hit hit any of the opponents ships
        for ship in playerShips:
            coords = ship.getCoordinates()
            if hit in coords:
                # checks if all coords of the opponents ship has been hit
                for i in coords:
                    row, col = i
                    if app.turn.boardHits[row][col] != 2:
                        return False
                completedShip(app, coords)
                app.player2.shipDestroyed()
                print(app.player2.destroyedShips)
                return True
            
    if app.turn.getId() == 2:
        # print("inside shipAllBombed2")
        playerShips = app.player1.ships
        # checks which ship was hit
        for ship in playerShips:
            # gets coords of ship
            coords = ship.getCoordinates()
            if hit in coords:
                # checks if all coords of the opponents ship has been hit
                for i in coords:
                    row, col = i
                    print(f"checking current coord = {i} = {app.turn.boardHits[row][col]}")
                    if app.turn.boardHits[row][col] != 2:
                        print("not all bombed")
                        return False
                completedShip(app, coords)
                print("is all bombed")
                app.player1.shipDestroyed()
                print(app.player1.destroyedShips)
                return True
            else:
                print("error")

# turns coords of ship to fully hit ship (gameplay)
def completedShip(app, coords):
    for i in coords:
        row, col = i
        app.turn.boardHits[row][col] = 3  
    if app.practice == True and app.turn.getId() == 2 and app.difficulty == "medium":
        outline = getOutline(app, coords)
        for i in outline:
            rowO, colO = i
            app.player2.boardHits[rowO][colO] == 0

def checkWin(app):
    # print(f"totShips = {app.totalShips}")
    # print(f"all ships destroyed {app.player2.destroyedShips}")
    if app.totalShips == app.player1.destroyedShips:
        app.winner = app.player2.getId()
        app.gameOver = True
    elif app.totalShips == app.player2.destroyedShips:
        # print("go in")
        app.winner = app.player1.getId()
        app.gameOver = True
    # print(f"game over = {app.gameOver}")  

#gui and graphics
# -----------------------------------------------------------------------------------------------

def gameDimensions():
    margin = 40
    # users can change this (make adjustable)
    rows = 15
    cols = 15
    cellSize = 35
    return (rows, cols, cellSize, margin) 

def appStarted(app):            # initialize the model (app.xyz)
    app.homepage = True
    app.multiplayer = False
    app.practice = False
    app.settings = False
    app.setup = False
    app.gameStarted = False
    app.ai = None

    app.difficulty = None

    app.winner = None
    app.gameOver = False
    (app.rows, app.cols, app.cellSize, app.margin) = gameDimensions()
    
    app.emptyColor = "light blue"
    app.selection = (-1, -1)
    
    bigShip = [
        [  True,  True,  True,  True ]
    ]
    medShip = [
        [  True,  True,  True]
    ]
    smallShip = [
        [  True,  True ]
    ]
    lShip = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    oShip = [
        [  True,  True ],
        [  True,  True ]
    ]
    uShip = [
        [  True,  False,  True ],
        [  True,  True,   True ]
    ]
    tShip = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    app.shipTypes = {1:bigShip, 2:medShip, 3:smallShip, 4:lShip, 5:oShip, 6:uShip, 7:tShip}
    app.shipNames = ["Big Ship", "Medium Ship", "Small Ship", "L Ship", "O Ship", "U Ship", "T Ship"]
    app.selectedShip = None

    #user can change this (make adjustable)  
    app.allShips = {1:1, 2:2, 3:3, 4:1, 5:2, 6:2, 7:1}
    
    app.totalShips = 0
    for key in app.allShips:
        app.totalShips += app.allShips[key]

    app.player1 = player(app, 1, app.rows, app.cols, app.emptyColor, app.allShips)
    app.player2 = player(app, 2, app.rows, app.cols, app.emptyColor, app.allShips)
    app.turn = app.player1
    initialShips(app, 1)
    app.turn = app.player2
    initialShips(app, 2)
    app.turn = app.player1

    # print(f"player1 ships{app.player1.ships}")
    # print(f"player2 ships{app.player2.ships}")

# creates all ships on the player's board depending on the player (both players will have different randomized boards)
def initialShips(app, player):
    if player == 1:
        for key in app.allShips:
            createShips(app, app.allShips[key], key, app.player1.ships)
    elif player == 2:
        for key in app.allShips:
            createShips(app, app.allShips[key], key, app.player2.ships)

    # if app.setup == True and app.turn.id == 1:
    #     for key in app.allShips:
    #         createShips(app, app.allShips[key], key, app.player1.ships)
    # elif app.setup == True and app.turn.id == 2:
    #     for key in app.allShips:
    #         createShips(app, app.allShips[key], key, app.player2.ships)

# randomizes the ship on the specifc player's board
def createShips(app, numberOfShips, shipType, playerShip):
    print(playerShip)
    print(shipType)
    type = app.shipTypes[shipType]
    row = len(type)
    col = len(type[0])

    names = []

    count = 0
    while True:
        while True:
            randRow = random.randint(0, app.rows-1)
            randCol = random.randint(0, app.cols-1)

            # creates Coords of current ship (rand on board)
            shipCoord = []
            for i in range(0, row):
                for j in range(0, col):
                    if type[i][j] == True:
                        shipCoord.append((randRow + i,randCol + j))
            
            # gets outline of ship
            outline = getOutline(app, shipCoord)
            if outline == False:
                break
            
            # checks if coords of point are legal, if legal add to app.ships
            if isShipLegal(app, shipCoord, outline) == True:
                if shipType == 1:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = bigShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)

                if shipType == 2:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = medShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)
                
                if shipType == 3:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = smallShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)

                if shipType == 4:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = lShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)

                if shipType == 5:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = oShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)

                if shipType == 6:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = uShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)

                if shipType == 7:
                    names.append(str(int(shipType)*10 + count))
                    names[0] = tShip(app, shipCoord, outline, shipType)
                    playerShip.append(names[0])

                    addCoords(app, shipCoord, shipType)
                    addOutline(app, outline)
                
                count += 1
                break
            else:
                break
        if count >= numberOfShips:
            break

# gets outline coords of ship when given the coordinates of the ship
def getOutline(app, shipCoord):
    directions = [(-1, -1), (0, -1), (1, -1), 
                    (-1, 0), (1, 0), 
                    (-1, 1), (0, 1), (1, 1)]

    outline = []
    for coord in shipCoord:
        row, col = coord
        for d in directions:
            rowD, colD = d
            newRow = row + rowD
            newCol = col + colD

            # checks if legal, if not, returns false
            if newRow > app.rows or newCol > app.cols:
                return False
            # checks if out of boarder by one, should still be ok since only ship cant exceed, thus wont append
            elif (newRow == app.rows or newCol == app.cols 
                    or (newRow, newCol) in shipCoord
                    or newRow == -1 or newCol == -1 ):
                continue
            # satisfy all constraints, appends coord of outline
            elif app.turn.getId() == 1:
                if app.player1.boardShips[newRow][newCol] < 0 and (newRow, newCol) not in outline:
                    outline.append((newRow, newCol)) 
            elif app.turn.getId() == 2:
                if app.player2.boardShips[newRow][newCol] < 0 and (newRow, newCol) not in outline:
                    outline.append((newRow, newCol)) 
    return outline

# checks if entire ship is legal      
def isShipLegal(app, shipCoord, outline):
    # checks if ship coords are legal
    for coordS in shipCoord:
        # print("ship false")
        rowS, colS = coordS
        if rowS < 0:
            print("f1")
            return False
        if colS < 0:
            print("f2")
            return False
        if rowS >= app.rows:
            print("f3")
            return False
        if colS >= app.cols:
            print("f4")
            return False
        if app.turn.boardShips[rowS][colS] >= 0:
            # print("f5")
            return False

    # checks if outline coords are legal
    for coordO in outline:
        print("outline False")
        rowO, colO = coordO
        if rowO < -1:
            return False
        if colO < -1:
            return False
        if rowO > app.rows:
            return False
        if colO > app.cols:
            return False
        if app.turn.boardShips[rowS][colS] > 0:
            print("f5")
            return False

    return True

# methods that draw the board
# -----------------------------------------------------------------------------------------------

# draws board on the left
def drawBoard1(app, canvas):
    if app.multiplayer == True:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell1(app, canvas, row, col, app.turn.board[row][col])
    elif app.practice == True:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell1(app, canvas, row, col, app.player1.board[row][col])

# draws board on the right           
def drawBoard2(app, canvas): 
    if app.multiplayer == True:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell2(app, canvas, row, col, app.turn.board[row][col])
    elif app.practice == True:
        for row in range(app.rows):
            for col in range(app.cols):
                drawCell2(app, canvas, row, col, app.player1.board[row][col])
    
# draws cells for the left board
def drawCell1(app, canvas, row, col, color):
    if app.setup == True:
        # canvas.create_rectangle(col*app.cellSize + app.width/2 - app.cellSize, 
        #                         row*app.cellSize + app.margin*(5/2),
        #                         (col + 1)*app.cellSize + app.width/2 + 35*app.cols/2, 
        #                         (row + 1)*app.cellSize + app.margin*(5/2), 
        #                         fill = color, 
        #                         width = 2)
        canvas.create_rectangle(col*app.cellSize + app.margin, 
                                row*app.cellSize + app.margin*(5/2),
                                (col + 1)*app.cellSize + app.margin, 
                                (row + 1)*app.cellSize + app.margin*(5/2), 
                                fill = color, 
                                width = 2)
    elif app.gameStarted == True:
        canvas.create_rectangle(col*app.cellSize + app.margin, 
                                row*app.cellSize + app.margin*(5/2), 
                                (col + 1)*app.cellSize + app.margin, 
                                (row + 1)*app.cellSize + app.margin*(5/2), 
                                fill = color, 
                                width = 2)
        canvas.create_text(col*app.cellSize + app.margin + 15, 
                            row*app.cellSize + app.margin*(5/2) + 20,
                            text = f"{row,col}",
                            font = "arial 10",
                            fill = "black")

 # draws cells for the right board       
def drawCell2(app, canvas, row, col, color):
    canvas.create_rectangle(col*app.cellSize + app.margin*2 + app.cols*app.cellSize, 
                            row*app.cellSize + app.margin*(5/2), 
                            (col + 1)*app.cellSize + app.margin*2 + app.cols*app.cellSize, 
                            (row + 1)*app.cellSize + app.margin*(5/2), 
                            fill = color, 
                            width = 2)

# draws circles for the left board
def drawCircle1(app, canvas, row, col, color):
    canvas.create_oval(col*app.cellSize + app.margin + app.cellSize/4, 
                        row*app.cellSize + app.margin*(5/2) + app.cellSize/4,
                        (col + 1)*app.cellSize + app.margin - app.cellSize/4, 
                        (row + 1)*app.cellSize + app.margin*(5/2) - app.cellSize/4, 
                        fill = color, 
                        width = 2)

# draws circles for the right board 
def drawCircle2(app, canvas, row, col, color):
    canvas.create_oval(col*app.cellSize + app.margin*2 + app.cols*app.cellSize + app.cellSize/4, 
                        row*app.cellSize + app.margin*(5/2) + app.cellSize/4, 
                        (col + 1)*app.cellSize + app.margin*2 + app.cols*app.cellSize - app.cellSize/4, 
                        (row + 1)*app.cellSize + app.margin*(5/2) - app.cellSize/4, 
                        fill = color, 
                        width = 2)

# methods that draw the ships and hits
# -----------------------------------------------------------------------------------------------

# draws all ships
def drawShips(app, canvas):
    # print(f"current ships = {app.turn.ships}")
    if app.multiplayer:
        if app.setup == True:
            for ship in app.turn.ships:
                    coords = ship.getCoordinates()
                    for coord in coords:
                        row, col = coord
                        drawCell1(app, canvas, row, col, "grey")
            
            # # only for testing outline
            # for row in range(len(app.turn.boardShips)):
            #     for col in range(len(app.turn.boardShips[0])):
            #         if app.turn.boardShips[row][col] == 0:
            #             drawCell1(app, canvas, row, col, "red")
        
        elif app.gameStarted == True:
            for ship in app.turn.ships:
                coords = ship.getCoordinates()
                for coord in coords:
                    row, col = coord
                    drawCell1(app, canvas, row, col, "grey")

    elif app.practice == True:
        if app.setup == True:
            for ship in app.player1.ships:
                    coords = ship.getCoordinates()
                    for coord in coords:
                        row, col = coord
                        drawCell1(app, canvas, row, col, "grey")
            
            # only for testing outline
            for row in range(len(app.player1.boardShips)):
                for col in range(len(app.player1.boardShips[0])):
                    if app.player1.boardShips[row][col] == 0:
                        drawCell1(app, canvas, row, col, "red")    
        
        elif app.gameStarted == True:
            for ship in app.player1.ships:
                coords = ship.getCoordinates()
                for coord in coords:
                    row, col = coord
                    drawCell1(app, canvas, row, col, "grey")

# draws the current players previous hits
def drawsHits(app, canvas):
    if app.multiplayer == True:
        board = app.turn.boardHits
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 1:
                    drawCircle2(app, canvas, row, col, "light gray")
                if board[row][col] == 2:
                    drawCircle2(app, canvas, row, col, "red")
                if board[row][col] == 3:
                    drawCell2(app, canvas, row, col, "black")
    
    elif app.practice == True:
        board = app.player1.boardHits
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 1:
                    drawCircle2(app, canvas, row, col, "light gray")
                if board[row][col] == 2:
                    drawCircle2(app, canvas, row, col, "red")
                if board[row][col] == 3:
                    drawCell2(app, canvas, row, col, "black")

# draws where the opponent has hit the currentt player
def drawOpponentHits(app, canvas):
    if app.multiplayer == True:
        if app.turn.getId() == 1:
            hits = app.player2.boardHits
            for row in range(len(hits)):
                for col in range(len(hits[0])):
                    if hits[row][col] > 0:
                        drawCircle1(app, canvas, row, col, "black")
        if app.turn.getId() == 2:
            hits = app.player1.boardHits
            for row in range(len(hits)):
                for col in range(len(hits[0])):
                    if hits[row][col] > 0:
                        drawCircle1(app, canvas, row, col, "black")

    elif app.practice == True:
        hits = app.player2.boardHits
        for row in range(len(hits)):
            for col in range(len(hits[0])):
                if hits[row][col] > 0:
                    drawCircle1(app, canvas, row, col, "black")

# text and titles
# -----------------------------------------------------------------------------------------------

# components in setup page
# -------------------------------
def sideBar(app, canvas):
    #create buttons for all Ships (say how many Ships there are)
    #when press button, will generate ship on board, 
        #then can move ship with arrow keys or drag idk
    
    canvas.create_text(app.margin*2 + app.cols*app.cellSize + app.cellSize*5/2,
                        app.margin*2 + app.margin*(1/2) + 50/2,
                        text = "Your Ships!",
                        font = "arial 25 bold",
                        fill = "black")
    
    canvas.create_rectangle(app.margin*2 + app.cols*app.cellSize, 
                            app.margin*2 + app.margin*(1/2) + 60,
                            app.margin*2 + app.cellSize*5 + app.cols*app.cellSize,
                            app.margin*2 + app.margin*(1/2) + (app.cellSize+30)*len(app.shipNames),
                            fill = "light gray")
    
    for i in range(len(app.shipNames)):
        canvas.create_text(app.margin*2 + app.cols*app.cellSize + app.cellSize*5/2,
                            (app.margin + 50/3)*(i+1) + 60 + app.margin*(3/2),
                            text = (f"{app.shipNames[i]} = {app.allShips[i+1]}"), 
                            font = "arial 15",
                            fill = "black")
    
    # button height = 50
    canvas.create_rectangle(app.margin*2 + app.cols*app.cellSize, 
                            app.margin*2 + app.margin*(1/2) + app.rows*app.cellSize - 50,
                            app.margin*2 + app.cellSize*5 + app.cols*app.cellSize,
                            app.margin*2 + app.margin*(1/2) + app.rows*app.cellSize,
                            fill = "light green",
                            outline = "black",
                            width = 2) 
                            
    canvas.create_text(app.margin*2 + app.cols*app.cellSize + app.cellSize*5/2,
                            app.margin*(5/2) + app.rows*app.cellSize - 25,
                            text = "Start Game", 
                            font = "arial 18 bold",
                            fill = "black")

# in multiple pages
# -------------------------------    
def generalTitles(app, canvas):
    canvas.create_text(app.width/2, 
                        app.height*(5/4), 
                        text = f"Player {app.turn.getId()}'s Turn",
                        font = "arial 30 bold", 
                        fill = "black")

# in homepage
# -------------------------------
def homepage(app, canvas):
    if app.homepage == True:
        canvas.create_text(app.width/2, 
                            app.height*(1/3), 
                            text = "Battle Ship!",
                            font = f"arial {app.rows*5} bold", 
                            fill = "black")
        
        canvas.create_rectangle(app.width*(2/7),
                                app.height*(1/4) + app.height*(1/6) + + app.height*(1/20),
                                app.width*(5/7),
                                app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/20),
                                fill = "light gray",
                                outline = "black")
        
        canvas.create_rectangle(app.width*(2/7),
                                app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + app.height*(1/10),
                                app.width*(5/7),
                                app.height*(1/4) + app.height*(1/6) + app.height*(2/7) + app.height*(1/10),
                                fill = "light gray",
                                outline = "black")
        
        canvas.create_text(app.width*(2/7) + app.width*(3/14),
                            app.height*(1/4) + app.height*(1/6) + + app.height*(1/20) + app.height*(1/14),
                            text = "Multiplayer",
                            font = "arial 25 bold")
        canvas.create_text(app.width*(2/7) + app.width*(3/14),
                            app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + app.height*(1/10) + app.height*(1/14),
                            text = "Practice",
                            font = "arial 25 bold")

def settings(app, canvas):
    canvas.create_text(app.width/2, 
                        app.height*(1/3), 
                        text = "Settings!",
                        font = f"arial {app.rows*4} bold", 
                        fill = "black")
    canvas.create_text(app.width/2, 
                        app.height*(1/3) + app.height*(1/10), 
                        text = "Difficulty",
                        font = f"arial 25 bold", 
                        fill = "black")
    # easy button
    canvas.create_rectangle(app.width*(1/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + + app.height*(1/10),
                            app.width*(3/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10),
                            fill = "light green",
                            outline = "black")
    canvas.create_text(app.width*(1/9) - app.width*(1/18) + app.width*(2/18),
                        app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) + app.height*(1/14),
                        text = "Easy",
                        font = f"arial 25 bold", 
                        fill = "black")
    # medium button
    canvas.create_rectangle(app.width*(4/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + + app.height*(1/10),
                            app.width*(6/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10),
                            fill = "yellow",
                            outline = "black")
    canvas.create_text(app.width*(4/9) - app.width*(1/18) + app.width*(2/18),
                        app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) + app.height*(1/14),
                        text = "Medium",
                        font = f"arial 25 bold", 
                        fill = "black")
    # hard button
    canvas.create_rectangle(app.width*(7/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + + app.height*(1/10),
                            app.width*(9/9) - app.width*(1/18),
                            app.height*(1/4) + app.height*(1/6) + app.height*(1/7) + + app.height*(1/10),
                            fill = "red",
                            outline = "black")
    canvas.create_text(app.width*(7/9) - app.width*(1/18) + app.width*(2/18),
                        app.height*(1/4) + app.height*(1/6) + + app.height*(1/10) + app.height*(1/14),
                        text = "Hard",
                        font = f"arial 25 bold", 
                        fill = "black")
    
# -----------------------------------------------------------------------------------------------
def redrawAll(app, canvas):
    if app.homepage == True:
        homepage(app, canvas)
    elif app.settings == True:
        settings(app, canvas)
    elif app.setup == True:
        if app.multiplayer == True:
            generalTitles(app, canvas)
        drawBoard1(app, canvas)
        sideBar(app, canvas)
        drawShips(app, canvas)
    elif app.gameStarted == True:
        if app.multiplayer == True:
            generalTitles(app, canvas)
        drawBoard1(app,canvas)
        drawBoard2(app, canvas)
        drawShips(app, canvas)
        drawsHits(app, canvas)
        drawOpponentHits(app, canvas)

    if app.gameOver == True:
        canvas.create_rectangle(app.width/2 - app.width/4,
                                app.height/2 - app.height/4, 
                                app.width/2 + app.width/4,
                                app.height/2 + app.height/4, 
                                fill="tan")
        canvas.create_text(app.height/2 - app.height/8, 
                            app.width/2, 
                            text = "Game Over",
                            font = "arial 35 bold")
        canvas.create_text(app.height/2 + app.height/20, 
                            app.width/2, 
                            text = f"Player {app.winner} Wins!",
                            font = "arial 35 bold")


def playBattleship():
    rows, cols, cellSize, margin = gameDimensions()
    
    width = (cols*cellSize)*2 + margin*3
    height = (rows*cellSize) + margin*4
    runApp(width=width, height=height)

def main():
    playBattleship()

if __name__ == '__main__':
    main()