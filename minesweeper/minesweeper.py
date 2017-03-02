# Script Name	: minesweeper.py
# Author		: Kadeem Nibbs
# Created		: 2/24/2017
# Last Modified	:
# Version		: 1.0

# This program runs a minesweepr game with a GUI made using TKinter.  The
# board dimensions and mine density are set to beginner level specifications.

from random import randrange
from Tkinter import *

class MinesweeperGame(object):
    instructions = """Left-click on a square to attempt to clear it if you
    think it does not hold a mine. Right-click on a square to flag it if you
    suspect that it holds a mine; the square will turn red to be easily
    noticeable and will become non-clickable.  Right-click on a flagged square
    to unflag it.  The game is lost when the player clicks on a square with
    a mine, and is won when the player clears every square on the board that
    does not contain a mine.  Good luck!!!
    """

    def __init__(self):
        self.field = [] # values in squares on field, opened squares have
        # have value set to None, non-negative integer value is number of
        # mines touching square, -1 means square has a mine
        self.rows = None # number of rows on field
        self.columns = None # number of columns on field
        self.mines = None # number of mines on field
        self.squaresCleared = None # number of squares player has cleared
        self.emptySquares = None # number of squares not containing mines
        self.GUI = Tk() # GUI
        self.GUIField = None # array for accessing GUI minefield widgets
        self.minesLabel = None # displays how many mines are left
        self.newGame = None # button to create new game
        self.f1 = None  # padding to center grid in GUI window
        self.fieldFrame = None  # frame holding field buttons

    def initialize_field(self):
        """Initialize field with mines placed randomly throughout."""
        self.rows = 9
        self.columns = 9
        self.field = [[0 for x in xrange(self.columns)] # rows*columns list
                            for y in xrange(self.rows)]
        self.mines = 10
        self.squaresCleared = 0
        self.emptySquares = (self.rows * self.columns) - self.mines
        minelocs = [] # stores tuples (row, column) of mine locations
        minesLeft = self.mines
        while minesLeft > 0: # scatter mines through grid
            row = randrange(self.rows)
            col = randrange(self.columns)
            if self.field[row][col] != -1: # if mine not placed here yet
                self.field[row][col] = -1
                minelocs.append((row,col))
                minesLeft -= 1
        self.initialize_counts(minelocs) # Count mines touching each square

    def initialize_counts(self, minelocs):
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

    def clear_square(self, event, loc):
        """Opens square at (row,column).  If the square is a mine, the game is
        lost.  If not, the square is opened.  If the square has mines touching
        it, the number of mines touching it is revealed.  If the square has
        value 0 continually check neighboring squares for 0's, if they have
        value 0, check their neighboring squares as well.  Clear every square
        surrounding squares with value 0.  Increment squaresCleared
        accordingly.
        """
        row = loc[0]
        col = loc[1]
        if self.field[row][col] == -1:
            self.show_square(row, col)
        if self.field[row][col] != 0:
            self.show_square(row, col)
        else:
            locs = [loc] # Attention. Below, row may no longer refer
                                  # to original function argument
            while locs: # while there are more 0-valued squares to visit
                row = locs[len(locs)-1][0] # peek at last square in field
                col = locs[len(locs)-1][1] # visited, get row and column
                self.show_square(row,col)
                locs.pop() # only visit each square once
                for rowOffset in xrange(-1,2): # check every neighbor square
                    for colOffset in xrange(-1,2):
                        r = row + rowOffset
                        c = col + colOffset
                        if r < 0 or c < 0: # not on field
                            continue
                        if r >= self.rows or c >= self.columns:
                            continue
                        if self.field[r][c] is None: # ignore opened square
                            continue
                        if self.field[r][c] == 0:
                            locs.append((r,c)) #visit next
                        self.show_square(r,c) # show all squares around 0

    def show_square(self, row, col):
        """Opens square at (row,col).  Triggers game over if the square is a
        mine, displays the opened square on the GUI otherwise.
        """
        val = self.field[row][col]
        if val is None: # ignore opened squares
            return
        elif val == -1: # player clicked on a mine =(
            self.minesLabel.configure(text="You lose!\n")
            self.minesLabel.configure(font=("Courier",16))
            self.game_over()
        elif val == 0: # display empty square
            square = Label(self.fieldFrame,text = "     ")
            square.grid(row=row,column=col,sticky=(N,E,W,S))
            self.field[row][col] = None
            self.squaresCleared += 1
            if self.squaresCleared == self.emptySquares: # player won =)
                self.minesLabel.configure(text="You win!!\n")
                self.minesLabel.configure(font=("Courier",16))
                self.game_won()
        else: # display number of mines touching square
            square = Label(self.fieldFrame,text="  %s  " % str(val))
            square.configure(highlightbackground="black")
            square.grid(row=row,column=col,sticky=(N,E,W,S))
            self.field[row][col] = None # show that square was opened
            self.squaresCleared += 1
            if self.squaresCleared == self.emptySquares:
                self.minesLabel.configure(text="You win!!\n")
                self.minesLabel.configure(font=("Courier",16))
                self.game_won()

    def flag_square(self, event, loc):
        """Flags square on GUI by changing its color and making it
        unclickable.  Destroys old widget at location specified by loc on GUI
        grid and replaces it.
        """
        row = loc[0]
        col = loc[1]
        flag = Button(self.fieldFrame,text="     ",bg="red")
        flag.grid(row=row,column=col,sticky=E)
        flag.bind('<Button-3>',lambda event,r=row,c=col:
                            self.unflag_square(event,(r,c)))
        self.GUIField[row][col].destroy() # destroy button there previously
        self.GUIField[row][col] = flag # store new button in GUIField
        self.mines -= 1
        self.minesLabel.configure(
            text=("Mines Remaining: %03d" % self.mines) + "\n\n"
            )

    def unflag_square(self, event, loc):
        """Unflags flagged square on GUI by changing its color and making it
        clickable.  Destroys old widget at location specified by loc on GUI
        grid and replaces it.
        """
        row = loc[0]
        col = loc[1]
        square = Button(self.fieldFrame,text="     ")
        square.grid(row=row,column=col,sticky=E)
        square.bind('<Button-1>', lambda event,r=row,c=col:
                            self.clear_square(event,(r,c)))
        square.bind('<Button-3>', lambda event,r=row,c=col:
                            self.flag_square(event,(r,c)))
        self.GUIField[row][col].destroy() # destroy button there previously
        self.GUIField[row][col] = square # store new button in GUIField
        self.mines += 1
        self.minesLabel.configure(
            text=("Mines Remaining: %03d" % self.mines) + "\n\n"
            )


    def game_over(self):
        """Reveals all mines in the mine field and unbinds all functions from
        mine field buttons.
        """
        for row in xrange(self.rows):
            for col in xrange(self.columns):
                if self.field[row][col] == -1:
                    square = Button(self.fieldFrame,text="     ",bg='red')
                    square.grid(row=row,column=col,sticky=E)
                    self.GUIField[row][col] = square
                self.GUIField[row][col].unbind('<Button-1>')
                self.GUIField[row][col].unbind('<Button-3>')

    def game_won(self):
        """Unbinds all functions from mine field buttons.  Preserves state of
        board.
        """
        for row in xrange(self.rows):
            for col in xrange(self.columns):
                self.GUIField[row][col].unbind('<Button-1>')
                self.GUIField[row][col].unbind('<Button-3>')

    def new_game(self, event):
        """Deletes all GUI widgets to prevent memory leaks from many games.
        Reinitializes field and GUI.
        """
        self.squaresCleared = 0
        self.minesLabel.destroy() # delete widgets to prevent memory leaks
        self.f1.destroy()
        self.fieldFrame.destroy()
        self.initialize_field()
        self.initialize_GUI()

    def initialize_GUI(self):
        """Initilizes GUI with buttons on mine field.  Binds each button with
        functions to open left-clicked squares and flag right-clicked squares.
        Stores access to the mine field buttons in GUIField.
        """
        self.GUI.title('Minesweeper')
        self.GUI.geometry('600x600') # window dimensions in pixels
        self.f1 = Frame(self.GUI)
        self.f1.grid(row=0,sticky=(N,E,W,S))
        self.minesLabel = Label(
            self.GUI,
            text=("Mines Remaining: %03d" % self.mines) + "\n\n"
            )
        self.minesLabel.grid(row=0,sticky=W)
        self.newGame = Button(self.GUI,text="New Game")
        self.newGame.bind('<Button-1>', self.new_game)
        self.newGame.grid(row=0,column=1,sticky=E)

        self.GUIField = [[0 for y in xrange(self.columns)]
                            for x in xrange(self.rows)] # for accessing mine
                                                    # field widgets
        self.fieldFrame = Frame(self.GUI)
        self.fieldFrame.grid(row=1,column=1)
        for row in xrange(self.rows): # make mine field buttons, place in grid
            for col in xrange(self.columns):
                square = Button(self.fieldFrame,text="     ")
                square.grid(row=row,column=col,sticky=E)
                square.bind('<Button-1>',lambda event,r=row,c=col:
                                    self.clear_square(event,(r,c)))
                square.bind('<Button-3>', lambda event,
                        loc=(row,col): self.flag_square(event, loc))
                self.GUIField[row][col] = square

    def start_game(self):
        """Loads instruction screen with start game button.  Triggers
        the start of the game when the start game button is left-clicked.
        """
        instructionsLabel = Label(self.GUI,text=self.instructions)
        instructionsLabel.grid(row=0, sticky=W)
        startGame = Button(self.GUI,text="Start Game")
        startGame.grid(row=1,sticky=E)
        startGame.bind('<Button-1>',lambda event:
                                            (instructionsLabel.destroy(),
                                            self.initialize_GUI(),
                                            startGame.destroy()
                                            ))


if __name__ == "__main__":
    game = MinesweeperGame()
    game.initialize_field()
    game.start_game()
    game.GUI.mainloop()
