import Tkinter as tk
import random

import sys
sys.path.append('~/Library/Python/2.7/site-packages')

from drawingpanel import *

BOARD_HEIGHT = 300
BOARD_WIDTH = 300
BOX_SIZE = 20

NUMBER_MINES = ((BOARD_WIDTH / BOX_SIZE - 1)**2)//10 

class Game():

  def __init__(self):
    self.master = tk.Tk()
    self.panel = Canvas(self.master, width = BOARD_WIDTH, height = BOARD_HEIGHT + 100, bg = 'white')
    self.panel.pack()


     
  def game_over(self):

    self.master.unbind("<Button-1>")
    self.master.unbind("<Button-2>")

    self.b = Button(self.master, text = 'Play Again?', command = self.new_game)
    self.panel.create_text(BOARD_WIDTH/2, BOARD_HEIGHT + 40, text  = 'Game Over', fill = 'red') 
    self.b.pack()

  def new_game(self):

    self.master.destroy()

    main()


class Board(Game):

  def __init__(self, Game):
   
    self.game = Game

    self.__length = BOARD_HEIGHT/BOX_SIZE - 1
    self.__width = BOARD_WIDTH/BOX_SIZE -1

    self.__tiles = []
    
    row = []

    for i in range(self.__length):
      for j in range(self.__width):
        new_tile = Tile(i*BOX_SIZE, j*BOX_SIZE, BOX_SIZE)
        row.append(new_tile)

      self.__tiles.append(row)
      row = []


  def draw(self, panel):

    panel.delete(ALL)

    marked_mines = 0

    for row in self.__tiles:
      for tile in row:
        tile.draw(panel)
      
        if(tile.marked_mine):
          marked_mines += 1

    mines = NUMBER_MINES - marked_mines

    bottom_text = 'Mines left: ' + repr(mines)
    text_fill = 'black'

    panel.create_text(BOARD_WIDTH/2, BOARD_HEIGHT + 20, text  = bottom_text, fill = text_fill)


  # assign mines to random locations across the board. 
  def assign_mines(self):

    mines_to_assign = NUMBER_MINES

    while(mines_to_assign > 0):
      x_index = random.randint(0, len(self.__tiles)-1)
      y_index = random.randint(0, len(self.__tiles)-1)


      if(self.__tiles[x_index][y_index].is_mine == False):
        self.__tiles[x_index][y_index].is_mine = True
        mines_to_assign -= 1

        for i in range(-1, 2):
          for j in range(-1, 2):
            try:
              if((x_index + i >= 0) and (y_index + j >= 0)):
                self.__tiles[x_index + i][y_index + j].value += 1
            except IndexError:
              pass


  def show_neighbors(self, center_x, center_y):
  
    for i in range(-1, 2):
      for j in range(-1, 2):
        try:
          if(center_x + i >= 0) and (center_y + j >= 0):
            if(self.__tiles[center_x + i][center_y+ j].is_clicked == False):
              self.__tiles[center_x + i][center_y + j].show_self()

              if(self.__tiles[center_x + i][center_y+ j].value == 0):
                self.show_neighbors(center_x + i, center_y + j)

        except IndexError:  
          pass
        

  # reveals the tile that was clicked
  def left_click_event(self, event):
 
    print("HELLA LEFT CLIX")

    mouse_click = []

    mouse_click.append(event.x)
    mouse_click.append(event.y)

    box_index_x = (mouse_click[0] - 10) // BOX_SIZE
    box_index_y = (mouse_click[1] - 10) // BOX_SIZE

    try:
      self.__tiles[box_index_x][box_index_y].show_self()

      if(self.__tiles[box_index_x][box_index_y].value == 0):
        self.show_neighbors(box_index_x, box_index_y)

      if(self.__tiles[box_index_x][box_index_y].is_mine):
        game.game_over()

    except IndexError:
      pass

    
    self.draw(game.panel)

  # Marks the clicked square as a mine
  def right_click_event(self, event):

    print("HELLA RIGHT CLIX")

    mouse_click = []

    mouse_click.append(event.x)
    mouse_click.append(event.y)

    box_index_x = (mouse_click[0] - 10) // BOX_SIZE
    box_index_y = (mouse_click[1] - 10) // BOX_SIZE

    try:
      board.__tiles[box_index_x][box_index_y].marked_mine = True

    except IndexError:
      pass

    self.draw(game.panel)


class Tile():

  def __init__(self, x, y, size):
    self.__x_index = x
    self.__y_index = y
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
  def show_self(self):
    self.is_clicked = True
    self.marked_mine = False


def main():

  global mines, game, board

  game = Game()

  board = Board(game)
  board.assign_mines()

  game.master.bind("<Button-1>", board.left_click_event)
  game.master.bind("<Button-2>", board.right_click_event)


  board.draw(game.panel)

  game.master.mainloop()


main()
