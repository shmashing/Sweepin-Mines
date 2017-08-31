import tkinter as tk
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
    self.initialize_game() 


  def initialize_game(self):
    self.master = tk.Tk()
    self.master.wm_title("Mine Sweeper")

    self.panel = Canvas(self.master, width = BOARD_WIDTH, height = BOARD_HEIGHT + 100, bg = 'white')
    self.panel.pack()

    self.board = Board(self.panel)

    self.board.assign_mines()

    self.master.bind("<Button-1>", self.left_click_event)
    self.master.bind("<Button-2>", self.right_click_event)

     
  def game_over(self):

    self.master.unbind("<Button-1>")
    self.master.unbind("<Button-2>")

    self._new_game_button = Button(self.master, text = 'Play Again?', command = self.new_game)
    self._quit_button = Button(self.master, text = 'Exit', command = self.master.quit)

    self._new_game_button.pack()
    self._quit_button.pack()

  def new_game(self):

    self.master.destroy()

    self.initialize_game()
    self.board.draw()
    self.master.mainloop()

  # reveals the tile that was clicked
  def left_click_event(self, event):
 
    mouse_click = []

    mouse_click.append(event.x)
    mouse_click.append(event.y)

    box_index_x = (mouse_click[0] - 10) // BOX_SIZE
    box_index_y = (mouse_click[1] - 10) // BOX_SIZE

    try:
      self.board.show_tile(box_index_x, box_index_y)

      if(self.board.get_tile_value(box_index_x, box_index_y) == 0):
        self.board.show_neighbors(box_index_x, box_index_y)


      if(self.board.location_is_mine(box_index_x, box_index_y)):
        self.game_over()

    except IndexError:
      pass

    self.board.draw()

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

      if(not self.board.location_is_clicked(box_index_x, box_index_y)):
        if(not self.board.location_is_marked(box_index_x, box_index_y)):
          if(len(self.board.marked_mines) == NUMBER_MINES):
            x_index = self.board.marked_mines[0][0]
            y_index = self.board.marked_mines[0][1]
            self.board.mark_mine(x_index, y_index, False)
            self.board.marked_mines.pop(0)

      
          self.board.mark_mine(box_index_x, box_index_y, True)
          self.board.marked_mines.append([box_index_x, box_index_y])

        else:
          self.board.mark_mine(box_index_x, box_index_y, False)
          self.board.marked_mines.remove([box_index_x, box_index_y])

    except IndexError:
      pass

    self.board.draw()

    if(self.check_for_win()):
      self.game_over()


  def check_for_win(self):

    for mine in self.board.mines:
      if(not self.board.tiles[mine[0]][mine[1]].marked_mine):
        return(False)

    return(True)


class Board(Game):

  def __init__(self, panel):
   
    self._length = BOARD_HEIGHT//BOX_SIZE - 1
    self._width = BOARD_WIDTH//BOX_SIZE -1
    self._panel = panel

    self.tiles = []
    self.mines = []
    self.marked_mines = []
    
    row = []

    for i in range(self._length):
      for j in range(self._width):
        new_tile = Tile(i, j, BOX_SIZE)
        row.append(new_tile)

      self.tiles.append(row)
      row = []


  def draw(self):

    self._panel.delete(ALL)

    marked_mines = 0

    for row in self.tiles:
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
      x_index = random.randint(0, len(self.tiles)-1)
      y_index = random.randint(0, len(self.tiles)-1)


      if(self.tiles[x_index][y_index].is_mine == False):
        self.tiles[x_index][y_index].is_mine = True
        self.tiles[x_index][y_index].value = -1

        self.mines.append([x_index, y_index])

        mines_to_assign -= 1

  
        for neighbor in self.tiles[x_index][y_index].get_neighbors():
          if(not self.tiles[neighbor[0]][neighbor[1]].is_mine):
            self.tiles[neighbor[0]][neighbor[1]].value += 1


  def show_tile(self, tile_index_x, tile_index_y):
    self.tiles[tile_index_x][tile_index_y].show_self()

  def show_neighbors(self, center_x, center_y):
  
    for neighbor in self.tiles[center_x][center_y].get_neighbors():

      if(not self.tiles[neighbor[0]][neighbor[1]].is_mine):
        if(self.tiles[neighbor[0]][neighbor[1]].value == 0):
          if(not self.tiles[neighbor[0]][neighbor[1]].is_clicked):
            self.tiles[neighbor[0]][neighbor[1]].show_self()
            self.show_neighbors(neighbor[0], neighbor[1]) 

        else:
          self.tiles[neighbor[0]][neighbor[1]].show_self()

  def get_tile_value(self, tile_index_x, tile_index_y):

    return(self.tiles[tile_index_x][tile_index_y].value)

  def location_is_clicked(self, tile_index_x, tile_index_y):

    if(self.tiles[tile_index_x][tile_index_y].is_clicked):
      return True

    return False

  def location_is_mine(self, tile_index_x, tile_index_y):

    if(self.tiles[tile_index_x][tile_index_y].is_mine):
      return(True)

    return(False)

  def location_is_marked(self, tile_index_x, tile_index_y):

    if(self.tiles[tile_index_x][tile_index_y].marked_mine):
      return(True)

    return(False)

  def mark_mine(self, tile_index_x, tile_index_y, mark):

    if(mark):
      self.tiles[tile_index_x][tile_index_y].marked_mine = True

    else:
      self.tiles[tile_index_x][tile_index_y].marked_mine = False
      

class Tile():

  def __init__(self, x, y, size):
    self._x_index = x
    self._y_index = y
    self._x = (x*size) + 10
    self._y = (y*size)  + 10
    self._size = size

    self.is_clicked = False
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
			       self._y + self._size/2, fill = 'red') 

        panel.create_line(self._x + 5, self._y + 5, self._x + 5, 
			  self._y + self._size - 2)

    else:
      if(self.is_mine):
        panel.create_rectangle(self._x, self._y, self._x + self._size, 
			       self._y + self._size, fill = 'red')

        panel.create_oval(self._x + (self._size/4), self._y + (self._size/4), 
                               self._x + 3*(self._size/4), self._y + 3*(self._size/4), fill = 'black')

        panel.create_line(self._x + (self._size/4) - 3, self._y + (self._size/2),
                               self._x + 3*(self._size/4) + 3, self._y + (self._size/2), fill = 'black')

        panel.create_line(self._x + (self._size/2), self._y + (self._size/4) - 3,
                               self._x + (self._size/2), self._y + 3*(self._size/4) + 3, fill = 'black')

        panel.create_line(self._x + (self._size/4) - 1.5, self._y + (self._size/4) - 1.5,
                               self._x + 3*(self._size/4) + 1, self._y + 3*(self._size/4) + 1, fill = 'black')

        panel.create_line(self._x + (self._size/4) - 1.5, self._y + 3*(self._size/4) + 1,
                               self._x + 3*(self._size/4) + 1, self._y + (self._size/4) - 1, fill = 'black')

        panel.create_rectangle(self._x + (self._size/4) + 2, self._y + (self._size/4) + 2,
                               self._x + (self._size/4) + 5, self._y + (self._size/4) + 5, fill = 'white')
        


      
      else:
        panel.create_rectangle(self._x, self._y, self._x + self._size, 
			       self._y + self._size, fill = 'grey')

        if(self.value != 0):
          self.get_color()
          panel.create_text(self._x + self._size/2, self._y + self._size/2,
			         text = str(self.value), fill = self.color)

  def get_color(self):

    colors = ['blue', 'dark green', 'red', 'purple', 'orange', 'cyan', 'dark red', 'black']

    self.color = colors[self.value - 1]

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

  game.board.draw()

  game.master.mainloop()


main()
