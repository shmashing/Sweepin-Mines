import Tkinter as tk
import random

import sys
sys.path.append('~/Library/Python/2.7/site-packages')

from drawingpanel import *

BOARD_HEIGHT = 300
BOARD_WIDTH = 300
BOX_SIZE = 20

NUMBER_MINES = int(((BOARD_WIDTH / BOX_SIZE - 1)**2) * 0.15)

class Game():

  def __init__(self):
    self._master = tk.Tk()
    self._master.wm_title("Mine Sweeper")
 
    self._panel = Canvas(self._master, width = BOARD_WIDTH, height = BOARD_HEIGHT + 100, bg = 'white')
    self._panel.pack()

    self._board = Board(self._panel)

    self._board.assign_mines()

    self._master.bind("<Button-1>", self.left_click_event)
    self._master.bind("<Button-2>", self.right_click_event)

     
  def game_over(self):

    self._master.unbind("<Button-1>")
    self._master.unbind("<Button-2>")

    self._new_game_button = Button(self._master, text = 'Play Again?', command = self.new_game)
    self._quit_button = Button(self._master, text = 'Exit', command = self._master.quit)

    self._new_game_button.pack()
    self._quit_button.pack()

  def new_game(self):

    self._master.destroy()

    self.__init__()
    self._board.draw()
    self._master.mainloop()

  # reveals the tile that was clicked
  def left_click_event(self, event):
 
    mouse_click = []

    mouse_click.append(event.x)
    mouse_click.append(event.y)

    box_index_x = (mouse_click[0] - 10) // BOX_SIZE
    box_index_y = (mouse_click[1] - 10) // BOX_SIZE

    try:
      self._board.show_tile(box_index_x, box_index_y)

      if(self._board.get_tile_value(box_index_x, box_index_y) == 0):
        self._board.show_neighbors(box_index_x, box_index_y)


      if(self._board.location_is_mine(box_index_x, box_index_y)):
        self.game_over()

    except IndexError:
      pass

    self._board.draw()

    if(self.check_for_win()):
      self.game_over()


  # Marks the clicked square as a mine
  def right_click_event(self, event):

    mouse_click = []

    mouse_click.append(event.x)
    mouse_click.append(event.y)

    box_index_x = (mouse_click[0] - 10) // BOX_SIZE
    box_index_y = (mouse_click[1] - 10) // BOX_SIZE

    try:

      if(not self._board.location_is_marked(box_index_x, box_index_y)):
        if(len(self._board._marked_mines) == NUMBER_MINES):
          x_index = self._board._marked_mines[0][0]
          y_index = self._board._marked_mines[0][1]
          self._board.mark_mine(x_index, y_index, False)
          self._board._marked_mines.pop(0)

      
        self._board.mark_mine(box_index_x, box_index_y, True)
        self._board._marked_mines.append([box_index_x, box_index_y])

      else:
        self._board.mark_mine(box_index_x, box_index_y, False)
        self._board._marked_mines.remove([box_index_x, box_index_y])

    except IndexError:
      pass

    self._board.draw()

    if(self.check_for_win()):
      self.game_over()


  def check_for_win(self):

    for mine in self._board._mines:
      if(not self._board._tiles[mine[0]][mine[1]].marked_mine):
        return(False)

    return(True)


class Board(Game):

  def __init__(self, panel):
   
    self._length = BOARD_HEIGHT/BOX_SIZE - 1
    self._width = BOARD_WIDTH/BOX_SIZE -1
    self._panel = panel

    self._tiles = []
    self._mines = []
    self._marked_mines = []
    
    row = []

    for i in range(self._length):
      for j in range(self._width):
        new_tile = Tile(i, j, BOX_SIZE)
        row.append(new_tile)

      self._tiles.append(row)
      row = []


  def draw(self):

    self._panel.delete(ALL)

    marked_mines = 0

    for row in self._tiles:
      for tile in row:
        tile.draw(self._panel)
      
        if(tile.marked_mine):
          marked_mines += 1

    mines = NUMBER_MINES - marked_mines
    
    if(mines < 0):
      mines = 0

    bottom_text = 'Mines left: ' + repr(mines)
    text_fill = 'black'

    self._panel.create_text(BOARD_WIDTH/2, BOARD_HEIGHT + 20, text  = bottom_text, fill = text_fill)


  # assign mines to random locations across the board. 
  def assign_mines(self):

    mines_to_assign = NUMBER_MINES

    while(mines_to_assign > 0):
      x_index = random.randint(0, len(self._tiles)-1)
      y_index = random.randint(0, len(self._tiles)-1)


      if(self._tiles[x_index][y_index].is_mine == False):
        self._tiles[x_index][y_index].is_mine = True
        self._tiles[x_index][y_index].value = -1

        self._mines.append([x_index, y_index])

        mines_to_assign -= 1

  
      for neighbor in self._tiles[x_index][y_index].get_neighbors():
        if(not self._tiles[neighbor[0]][neighbor[1]].is_mine):
          self._tiles[neighbor[0]][neighbor[1]].value += 1


  def show_tile(self, tile_index_x, tile_index_y):
    self._tiles[tile_index_x][tile_index_y].show_self()

  def show_neighbors(self, center_x, center_y):
  
    for neighbor in self._tiles[center_x][center_y].get_neighbors():

      if(not self._tiles[neighbor[0]][neighbor[1]].is_mine):
        if(self._tiles[neighbor[0]][neighbor[1]].value == 0):
          if(not self._tiles[neighbor[0]][neighbor[1]].is_clicked):
            self._tiles[neighbor[0]][neighbor[1]].show_self()
            self.show_neighbors(neighbor[0], neighbor[1]) 

        else:
          self._tiles[neighbor[0]][neighbor[1]].show_self()

  def get_tile_value(self, tile_index_x, tile_index_y):

    return(self._tiles[tile_index_x][tile_index_y].value)


  def location_is_mine(self, tile_index_x, tile_index_y):

    if(self._tiles[tile_index_x][tile_index_y].is_mine):
      return(True)

    return(False)

  def location_is_marked(self, tile_index_x, tile_index_y):

    if(self._tiles[tile_index_x][tile_index_y].marked_mine):
      return(True)

    return(False)

  def mark_mine(self, tile_index_x, tile_index_y, mark):

    if(mark):
      self._tiles[tile_index_x][tile_index_y].marked_mine = True

    else:
      self._tiles[tile_index_x][tile_index_y].marked_mine = False
      

class Tile():

  def __init__(self, x, y, size):
    self._x_index = x
    self._y_index = y
    self._x = (x*size) + 10
    self._y = (y*size)  + 10
    self._size = size

    self.is_clicked = True
    self.is_mine = False
    self.marked_mine = False
    self.value = 0

  # Tile function to draw itself to the window. 
  def draw(self, panel):

    # If the tile has yet to be clicked, draw a dark gray box on top of a light gray box
    # If the tile is marked as a mine, draw a cute lil flag on there
    if(self.is_clicked == False):
      panel.create_rectangle(self._x, self._y, self._x + self._size, 
			     self._y + self._size, fill = 'grey')

      panel.create_line(self._x, self._y, self._x + self._size, 
			self._y + self._size, fill = 'dim grey')

      panel.create_line(self._x, self._y + self._size, self._x + self._size,
			self._y, fill = 'dim grey')

      panel.create_rectangle(self._x + 2, self._y + 2, self._x + self._size - 2, 
			     self._y + self._size - 2, fill = 'dim grey', outline = 'dim grey')

      if(self.marked_mine):
        panel.create_rectangle(self._x + 5, self._y + 5, self._x + self._size - 5, 
			       self._y + self._size/2, fill = 'black') 

        panel.create_line(self._x + 5, self._y + 5, self._x + 5, 
			  self._y + self._size - 2)

    else:
      if(self.is_mine):
        panel.create_rectangle(self._x, self._y, self._x + self._size, 
			       self._y + self._size, fill = 'grey')
        panel.create_line(self._x, self._y, self._x + self._size, 
			  self._y + self._size, fill = 'red')
        panel.create_line(self._x, self._y + self._size, self._x + self._size,
			  self._y, fill = 'red')
        panel.create_line(self._x, self._y + self._size/2, self._x + self._size, 
			  self._y + self._size/2, fill = 'red')
        panel.create_line(self._x + self._size/2, self._y, self._x + self._size/2, 
			  self._y + self._size, fill = 'red')
      
      else:
        panel.create_rectangle(self._x, self._y, self._x + self._size, 
			       self._y + self._size, fill = 'grey')

        if(self.value != 0):
          panel.create_text(self._x + self._size/2, self._y + self._size/2,
			         text = str(self.value))

  # Tile function to reveal a tile. 
  def show_self(self):
    self.is_clicked = True
    self.marked_mine = False

  # gathers all real neighbors and returns a list of their indices
  def get_neighbors(self):

    neighbors = []

    for i in range(-1, 2):
      for j in range(-1, 2):

        if(0 <= (self._x_index + i) < (BOARD_WIDTH/BOX_SIZE - 1)):
          if(0 <= (self._y_index + j) < (BOARD_WIDTH/BOX_SIZE -1)):
            if(not(i == 0 and j == 0)):
              neighbors.append([self._x_index + i, self._y_index + j])

    return(neighbors)


def main():

  game = Game()

  game._board.draw()

  game._master.mainloop()


main()
