from enum import Enum
from tile import Tile, TileSide
import pygame, colors, settings, move
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, PieceSide
from settings import SQUARE_SIZE

# TODO: remove pieces form this and put it into a broader manager class.

class Board:

    perspective_white = True

    tiles = [[]]

    def __init__(self):

        for x in range(8):
            self.tiles.append([])
            for y in range(8):
                side = TileSide.DARK
                if (x+y)%2 == 0:
                    side = TileSide.LIGHT
                self.tiles[x].append(Tile(x, y, side))

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                y_adjusted = tile.y
                if self.perspective_white:
                    y_adjusted = abs(y_adjusted-7)

                pygame.draw.rect(surface, tile.get_color(), (tile.x*SQUARE_SIZE, y_adjusted*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def click(self, pos):

        x_pos = pos[0]
        y_pos = pos[1]

        x, y = self.convert_coords_into_indecies(x_pos, y_pos)

        #Inverts the y value if the perspective is white.
        if self.perspective_white:
            y = abs(7-y)

        return x,y

    def convert_coords_into_indecies(self, x_pos, y_pos):
        x = int(x_pos / settings.SQUARE_SIZE)
        y = int(y_pos / settings.SQUARE_SIZE)
        return x, y

    def deselect(self):
        for row in self.tiles:
            for tile in row:
                tile.selected = False
                tile.highlighted = False

