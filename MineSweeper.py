import Tkinter as tk
import random
import sys
sys.path.append('~/Library/Python/2.7/site-packages')

from drawingpanel import *

BOARD_HEIGHT = 300
BOARD_WIDTH = 300
BOX_SIZE = 20
#board = []

NUMBER_MINES = ((BOARD_WIDTH / BOX_SIZE - 1)**2)//10 

class Tile():

  def __init__(self, x, y, size):
    self.__x = x + 10
    self.__y = y  + 10
    self.__size = size

    self.is_clicked = False
    self.is_mine = False
    self.marked_mine = False
    self.value = 0

  # Tile function to draw itself to the window. 
  def draw(self, panel):

    # If the tile has yet to be clicked, draw a dark gray box on top of a light gray box
    # If the tile is marked as a mine, draw a cute lil flag on there
    if(self.is_clicked == False):
      panel.create_rectangle(self.__x, self.__y, self.__x + self.__size, 
			     self.__y + self.__size, fill = 'grey')

      panel.create_line(self.__x, self.__y, self.__x + self.__size, 
			self.__y + self.__size, fill = 'dim grey')

      panel.create_line(self.__x, self.__y + self.__size, self.__x + self.__size,
			self.__y, fill = 'dim grey')

      panel.create_rectangle(self.__x + 2, self.__y + 2, self.__x + self.__size - 2, 
			     self.__y + self.__size - 2, fill = 'dim grey', outline = 'dim grey')

      if(self.marked_mine):
        panel.create_rectangle(self.__x + 5, self.__y + 5, self.__x + self.__size - 5, 
			       self.__y + self.__size/2, fill = 'black') 

        panel.create_line(self.__x + 5, self.__y + 5, self.__x + 5, 
			  self.__y + self.__size - 2)

    else:
      if(self.is_mine):
        panel.create_rectangle(self.__x, self.__y, self.__x + self.__size, 
			       self.__y + self.__size, fill = 'grey')
        panel.create_line(self.__x, self.__y, self.__x + self.__size, 
			  self.__y + self.__size, fill = 'red')
        panel.create_line(self.__x, self.__y + self.__size, self.__x + self.__size,
			  self.__y, fill = 'red')
        panel.create_line(self.__x, self.__y + self.__size/2, self.__x + self.__size, 
			  self.__y + self.__size/2, fill = 'red')
        panel.create_line(self.__x + self.__size/2, self.__y, self.__x + self.__size/2, 
			  self.__y + self.__size, fill = 'red')
      
      else:
        panel.create_rectangle(self.__x, self.__y, self.__x + self.__size, 
			       self.__y + self.__size, fill = 'grey')

        if(self.value != 0):
          panel.create_text(self.__x + self.__size/2, self.__y + self.__size/2,
			         text = str(self.value))

  # Tile function to reveal a tile. 
  def show_self(self, x_index, y_index):
    self.is_clicked = True
    self.marked_mine = False

    # If the clicked tile has a value of zero, show all the neighbors that are
    # zero or 1
    if(self.value == 0):
      self.show_neighbors(x_index, y_index)

  # Tile function to show all neighbors that have yet to be revealed
  def show_neighbors(self, x_index, y_index):

    for i in range(-1, 2):
      for j in range(-1, 2):
        try:
          if(x_index + i >= 0) and (y_index + j >= 0):
            if(board[x_index + i][y_index + j].is_clicked == False):
              board[x_index + i][y_index + j].show_self(x_index + i, y_index + j)

        except IndexError:  
          pass

# set up the widget to the correct height/width and draw all the tiles and their
# current states to the board. 
#
# Parameters:   Booalean that controls whether the game is over or not
# Returns:      Nothing
def draw_board(game_over):

  panel.delete(ALL)

  marked_mines = 0

  for row in board:
    for tile in row:
      tile.draw(panel)
      
      if(tile.marked_mine):
        marked_mines += 1

  mines = NUMBER_MINES - marked_mines

  bottom_text = 'Mines left: ' + repr(mines)
  text_fill = 'black'

  panel.create_text(BOARD_WIDTH/2, BOARD_HEIGHT + 20, text  = bottom_text, fill = text_fill)


# assign mines to random locations across the board. 
def assign_mines(board):

  mines_to_assign = NUMBER_MINES

  while(mines_to_assign > 0):
    x_index = random.randint(0, len(board)-1)
    y_index = random.randint(0, len(board)-1)


    if(board[x_index][y_index].is_mine == False):
      board[x_index][y_index].is_mine = True
      mines_to_assign -= 1

      for i in range(-1, 2):
        for j in range(-1, 2):
          try:
            if((x_index + i >= 0) and (y_index + j >= 0)):
              board[x_index + i][y_index + j].value += 1
          except IndexError:
            pass

# When the user left-clicks, gather they x, y data and reveal the tile 
# that surrounds the coordinates.
def left_click_event(event):
 
  mouse_click = []

  mouse_click.append(event.x)
  mouse_click.append(event.y)

  box_index_x = (mouse_click[0] - 10) // BOX_SIZE
  box_index_y = (mouse_click[1] - 10) // BOX_SIZE

  try:
    board[box_index_x][box_index_y].show_self(box_index_x, box_index_y)
    
    if(board[box_index_x][box_index_y].is_mine):
      game_over()

  except IndexError:
    pass
  
  draw_board(False) 

# Right click event. Marks a square as a mine
def flag_square(event):

  mouse_click = []

  mouse_click.append(event.x)
  mouse_click.append(event.y)

  box_index_x = (mouse_click[0] - 10) // BOX_SIZE
  box_index_y = (mouse_click[1] - 10) // BOX_SIZE


  try:
    board[box_index_x][box_index_y].marked_mine = True


    draw_board(False)

  except IndexError:
    pass

    
def game_over():

  master.unbind("<Button-1>")
  master.unbind("<Button-2>")

  #draw_board(True)
  panel.create_text(BOARD_WIDTH/2, BOARD_HEIGHT + 40, text  = 'Game Over', fill = 'red') 

  b = Button(master, text = 'Play Again?', command = main)
  b.pack()

def main():

  global mines, master, panel, board

  try:
    if(master):
      master.delete(b)
      master.quit()
      panel.destroy()

  except NameError:
    pass

  board = []

  master = tk.Tk()

  panel = Canvas(master, width = BOARD_WIDTH, height = BOARD_HEIGHT + 100, bg = 'grey')
  panel.pack()

  mines = NUMBER_MINES

  boxes_x = BOARD_WIDTH / BOX_SIZE - 1
  boxes_y = BOARD_HEIGHT / BOX_SIZE - 1

  row = []

  for i in range(boxes_y):
    for j in range(boxes_x):
      new_tile = Tile(i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE)
      row.append(new_tile)

    board.append(row)
    row = []

  assign_mines(board)  

  draw_board(False)

  master.bind("<Button-1>", left_click_event)
  master.bind("<Button-2>", flag_square)

  master.mainloop()


main()
