from enum import Enum
from tile import Tile, TileSide
import pygame
import colors
import settings
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, PieceSide
from settings import SQUARE_SIZE


class Board:

    perspective_white = True

    selection = None
    tiles = [[]]
    pieces = []

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
                if tile.piece is not None :
                    tile.piece.draw(surface, self.perspective_white)

    def click(self, pos):

        x_pos = pos[0]
        y_pos = pos[1]

        x, y = self.convert_coords_into_indecies(x_pos, y_pos)

        if self.perspective_white:
            y = abs(7-y)

        if self.selection is not None:
            self.move_piece(x, y)
            self.deselect()

        elif self.tiles[x][y].piece is not None:
            self.select_piece(x, y)

    def select_piece(self, x, y):
        self.tiles[x][y].piece.highlight_possible_moves(self.tiles)
        self.tiles[x][y].click()
        self.selection = self.tiles[x][y].piece
        self.selection.highlight_possible_moves(self.tiles)

    def move_piece(self, x, y):
        if (self.tiles[x][y].piece is None or not self.tiles[x][y].piece.piece_side is self.selection.piece_side) and self.tiles[x][y].highlighted:
            # Remove old selection
            self.tiles[self.selection.x][self.selection.y].piece = None
            # Remove piece on Square
            if not self.tiles[x][y].piece is None:
                self.pieces.remove(self.tiles[x][y].piece)
            # Set new coords
            self.selection.move(x, y, self.tiles)
            # Add piece to new tile overriding old one if present
            self.tiles[x][y].piece = self.selection
            # Nullify board selection
        self.selection = None

    def convert_coords_into_indecies(self, x_pos, y_pos):
        x = int(x_pos / settings.SQUARE_SIZE)
        y = int(y_pos / settings.SQUARE_SIZE)
        return x, y

    def deselect(self):
        for row in self.tiles:
            for tile in row:
                tile.selected = False
                tile.highlighted = False

