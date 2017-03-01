# Script Name	: minesweeper.py
# Author		: Kadeem Nibbs
# Created		: 2/24/2017
# Last Modified	:
# Version		: 1.0

# This program runs a minesweepr game with a GUI made using TKinter.  The
# board dimensions and mine density are set to expert level specifications.

from random import randrange
from Tkinter import *
import time

class MinesweeperGame(object):

    def __init__(self):
        self.field = [] # values in squares on field, 0 means empty and
           # unopened, -1 means mine, non-zero positive integer is the number
           # of mines touching that square, None means empty and opened.
           # field will be set to specifications of expert level difficulty
        self.rows = 9 # number of rows on field
        self.columns = 9 # number of columns on field
        self.mines = None # number of mines on field
        self.squaresCleared = None
        self.emptySquares = None
        self.GUI = Tk()
        self.minesLabel = None # displays how many mines are left
        self.f1 = None  # padding to center grid in GUI window
        self.fieldFrame = None  # frame holding field buttons

    def initializeField(self):
        """Initialize field with mines placed randomly throughout."""

        self.field = [[0 for x in xrange(self.columns)]
                            for y in xrange(self.rows)]
        self.mines = 10
        self.squaresCleared = 0
        self.emptySquares = (self.rows * self.columns) - self.mines
        minelocs = []
        minesLeft = self.mines
        while minesLeft > 0: # scatter mines through grid
            row = randrange(self.rows)
            col = randrange(self.columns)
            if self.field[row][col] != -1: # if mine not placed here yet
                self.field[row][col] = -1
                minelocs.append((row,col))
                minesLeft -= 1
        self.initializeCounts(minelocs) # Count mines touching each square

    def initializeCounts(self, minelocs):
        """Gives each square on field the number of adjacent mines as its
        value, saves computational time by only visiting squares adjacent
        to mines.
        """

        for loc in minelocs:
            locs = [] # stores locations of squares adjacent to mines

            # Check every square adjacent to mine, if its value is 0, it does
            # not have a mine and it has not yet been visited, append its
            # location to locs
            row = loc[0]
            col = loc[1]
            for rowOffset in xrange(-1,2):
                for colOffset in xrange(-1,2):
                    r = row + rowOffset
                    c = col + colOffset
                    if r < 0 or c < 0:
                        continue
                    if r >= self.rows or c >= self.columns:
                        continue
                    if self.field[r][c] != 0:
                        continue
                    locs.append((r,c))
            for loc in locs:
                # check for mines touching square, increment mineCount for each
                # one
                row = loc[0]
                col = loc[1]
                mineCount = 0
                for rowOffset in xrange(-1,2):
                    for colOffset in xrange(-1,2):
                        r = row + rowOffset
                        c = col + colOffset
                        if r < 0 or c < 0: # square not on field
                            continue
                        if r >= self.rows or c >= self.columns:
                            continue
                        if self.field[r][c] == -1: # square has mine, count it
                            mineCount += 1
                self.field[row][col] = mineCount

    def clearSquare(self, event, loc):
        """Opens square at (row,column).  If the square is a mine, the game is
        lost.  If not, the square is opened.  If the square has mines touching
        it, the number of mines touching it is revealed.  If the square does
        not have any mines touching it (its value is 0), every contiguous
        square with value 0 is cleared as well.
        """
        print loc
        row = loc[0]
        col = loc[1]
        if self.field[row][col] == -1:
            self.showSquare(row, col)
            return -1 # Denotes game failure
        if self.field[row][col] != 0:
            self.showSquare(row, col)
        else:
            locs = [loc] # Attention. Below, row may no longer refer
                                  # to original function argument
            while locs: # while there are more squares to visit
                row = locs[len(locs)-1][0] # peek at last square in field
                col = locs[len(locs)-1][1] # visited, get row and column
                self.showSquare(row,col)
                locs.pop()
                for rowOffset in xrange(-1,2):
                    for colOffset in xrange(-1,2):
                        r = row + rowOffset
                        c = col + colOffset
                        if rowOffset == 0 and colOffset == 0:
                            continue
                        if r < 0 or c < 0:
                            continue
                        if r >= self.rows or c >= self.columns:
                            continue
                        if self.field[r][c] is None:
                            continue
                        if self.field[r][c] == 0:
                            locs.append((r,c))
                        self.showSquare(r,c)
                print locs

    def showSquare(self, row, col):
        val = self.field[row][col]
        if val is None:
            return
        elif val == -1:
            self.minesLabel.grid_forget()
            lossLabel = Label(self.GUI,text="You lose!!!!\n\n")
            lossLabel.grid(row=0)
            self.gameOver()
        elif val == 0:
            square = Label(self.fieldFrame,text = "     ")
            square.grid(row=row,column=col,sticky=(N,E,W,S))
            self.field[row][col] = None
            self.squaresCleared += 1
            if self.squaresCleared == self.emptySquares:
                minesLabel.configure(text="You win!")
                self.minesLabel.grid(row=0,sticky=W)
        else:
            square = Label(self.fieldFrame,text="  %s  " % str(val))
            square.grid(row=row,column=col,sticky=(N,E,W,S))
            self.field[row][col] = None
            self.squaresCleared += 1
            if self.squaresCleared == self.emptySquares:
                self.minesLabel.configure(text="You win!")
                self.minesLabel.grid(row=0,sticky=W)

    def flagSquare(self, event, loc):
        row = loc[0]
        col = loc[1]
        flag = Button(self.fieldFrame,bg="red")
        flag.grid(row=row,column=col,sticky=(N,E,W,S))
        flag.bind('<Button-3>',lambda event,r=row,c=col: self.unFlagSquare(event,(r,c)))
        self.mines -= 1
        self.minesLabel.configure(text="Mines Remaining: %s\n\n" % self.mines)

    def unFlagSquare(self, event, loc):
        row = loc[0]
        col = loc[1]
        flag = Button(self.fieldFrame,text="     ")
        flag.grid(row=row,column=col,sticky=(N,E,W,S))
        flag.bind('<Button-1>', lambda event,r=row,c=col: self.clearSquare(event,(r,c)))
        flag.bind('<Button-3>', lambda event,r=row,c=col: self.flagSquare(event,(r,c)))
        self.mines += 1
        self.minesLabel.configure(text="Mines Remaining: %s\n\n" % self.mines)

    def gameOver(self):
        time.sleep(5)
        for row in xrange(self.rows):
            for col in xrange(self.columns):
                square = Button(self.fieldFrame,text="     ",bg='red')
                square.grid(row=row,column=col,sticky=(N,E,W,S))

    def newGame(self, event):
        self.squaresCleared = 0
        self.initializeField()
        self.initializeGUI()

    def initializeGUI(self):
        self.GUI.title('Minesweeper')
        self.GUI.geometry('600x600') # window dimensions in pixels
        self.f1 = Frame(self.GUI)
        self.f1.grid(row=0,sticky=(N,E,W,S))
        self.minesLabel = Label(self.GUI,text="Mines Remaining: %s" %
                                self.mines + "\n\n")
        self.minesLabel.grid(row=0,sticky=W)
        newGame = Button(self.GUI,text="New Game")
        newGame.bind('<Button-1>', self.newGame)
        newGame.grid(row=0,column=1,sticky=E)

        filler = Label(self.GUI,text=" ") # move board away from window edge
        filler.grid(row=1,column=0)
        guiSquares = [[0 for y in xrange(self.columns)]
                            for x in xrange(self.rows)]
        self.fieldFrame = Frame(self.GUI)
        self.fieldFrame.grid(row=1,column=1,sticky=(N,E,W,S))

        for row in xrange(self.rows):
            for col in xrange(self.columns):
                square = Button(self.fieldFrame,text="     ")
                square.grid(row=row,column=col,sticky=(N,E,W,S))
                square.bind('<Button-1>',lambda event,r=row,c=col: self.clearSquare(event,(r,c)))
                square.bind('<Button-3>', lambda event,
                        loc=(row,col): self.flagSquare(event, loc))
                guiSquares[row][col] = square
