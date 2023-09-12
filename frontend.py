from tkinter import *
from classes import *
from random import randint
from tkinter import messagebox
from time import sleep
# Connect 4 board representation
# Board is a 2d array of None, 1s, and 2s
# None represents an empty space
# 1 represents a red piece
# 2 represents a yellow piece
# The board is 6 rows by 7 columns

class connect4 (Tk):
    '''Application class for Connect 4, derived from the base tkinter'''

    # Define standard colors used.
    RED = '#ff3838'
    BLUE = '#3e73de'
    YELLOW = '#fadb43'
    WHITE = 'white'
    GREEN = '#02ab13'

    # Define standard board parameters.
    ROWS = 6
    COLS = 7
    SIZE = 700
    sep = SIZE//7
    gap = sep/10
    # Define standard game parameters.
    bot_start = False
    bot_color = YELLOW
    bot_depth = 4
    done = False

    #defines the game board
    game_state = game()

    def __init__(self):
        super().__init__(None)
        self.canvas = Canvas(self, width=self.SIZE, height=self.SIZE, bg=self.BLUE) #creates the canvas
        self.canvas.pack() 
        self.title('Connect 4') #sets the title
        self.grid_d = {} #creates a dictionary to store the board
        for j in range(self.ROWS): #generates the board with empty spaces
            for i in range(self.COLS):
                self.grid_d[(i,j)] = self.canvas.create_oval(i*self.sep+self.gap,
                                                        j*self.sep+self.sep+self.gap,
                                                        i*self.sep+self.sep-self.gap,
                                                        j*self.sep+2*self.sep-self.gap, 
                                                        fill=self.WHITE)

        for k in range(self.COLS): #creates the buttons
            self.canvas.create_rectangle(k*self.sep,0,k*self.sep+self.sep,self.sep,fill=self.GREEN)
          
        if randint(1,2) == 1: #randomly chooses who goes first
            self.bot_color = self.RED
            a = self.game_state.move_bot(self.bot_depth)
            self.drop_animation(a, self.bot_color)
            self.bot_start = True
            self.update()

        self.canvas.bind("<Button-1>", lambda event: self.on_click(event))

    def place(self, row, col, color):
        """Places a piece of the given color at the given row and column."""
        self.canvas.itemconfig(self.grid_d[(row,col)], fill=color)
        
    def drop_piece(self, col):
        """Drops a piece in the given column and updates the game state."""
        self.game_state.move(col)
        if self.bot_start == True:
            self.drop_animation(col,self.YELLOW)
        else:
            self.drop_animation(col,self.RED)
        self.update()
        a = self.game_state.move_bot(4)
        self.drop_animation(a, self.bot_color)
        print(self.game_state.board.score)
        self.update()

    def on_click(self,event): 
        """Handles a click event on the canvas."""
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if y > self.sep:
            return
        i_button = x // self.sep
        self.drop_piece(int(i_button))
        return
    
    def drop_animation(self, col, color):
        """Animates a piece dropping into the given column."""
        row = 0
        while row < self.ROWS and self.game_state.board.state[row][col] == None:
            self.canvas.itemconfig(self.grid_d[(col,row)], fill=color) #changes the color of the piece
            self.canvas.update()
            row += 1
            sleep(0.20)
            self.canvas.itemconfig(self.grid_d[(col,row-1)], fill=self.WHITE) #changes back to color of the piece
            self.canvas.update()

    
    def update(self) -> None:
        """Updates the board to match the current game state. Only visual"""
        for i in self.game_state.board.state:
            for j in range(len(i)):
                if i[j] == 1:
                    self.place(j,self.game_state.board.state.index(i),self.RED)
                elif i[j] == 2:
                    self.place(j,self.game_state.board.state.index(i),self.YELLOW)
        self.canvas.update() #updates the canvas
        self.title(f'Connect 4 | Turn:{self.game_state.turn}') #updates the turn

        if self.game_state.board.won == True and self.done == False: #checks if the game is over
            self.done = True #prevents the message box from popping up multiple times
            self.canvas.unbind("<Button-1>") #unbinds the button
            if (self.game_state.board.score == 9999 and self.bot_start == True) or (self.game_state.board.score == -9999 and self.bot_start == False): #checks who won
                messagebox.showinfo("Game Over", "You lose!")
            elif (self.game_state.board.score == 9999 and self.bot_start == False) or (self.game_state.board.score == -9999 and self.bot_start == True):   
                messagebox.showinfo("Game Over", "You win!")    
            else:
                messagebox.showinfo("Game Over", "It's a tie!")
if __name__ == '__main__':
    app = connect4()
    app.mainloop()