from enum import Enum
import pygame
import colors
import settings
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, PieceSide
from settings import SQUARE_SIZE


class TileSide(Enum):
    LIGHT = 0
    DARK = 1


class Tile:

    piece = None
    selected = False
    highlighted = False

    x = 0
    y = 0
    tile_side = TileSide.LIGHT

    def __init__(self, x, y, tile_side):
        self.x = x
        self.y = y
        self.tile_side = tile_side

    def get_color(self):

        if self.selected:
            return colors.SELECTION

        if self.tile_side == TileSide.LIGHT:
            if self.highlighted:
                return colors.LIGHT_TILE_HIGHLIGHT
            else:
                return colors.LIGHT_TILE
        else:
            if self.highlighted:
                return colors.DARK_TILE_HIGHLIGHT
            else:
                return colors.DARK_TILE

    def click(self):
        self.selected = True


class Board:

    selection = None
    tiles = [[]]
    pieces = []

    def __init__(self):
        for y in range(8):
            self.tiles.append([])
            for x in range(8):
                side = TileSide.DARK
                if (x+y)%2 == 0:
                    side = TileSide.LIGHT
                self.tiles[y].append(Tile(x, y, side))

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(surface, tile.get_color(), (tile.x*SQUARE_SIZE, tile.y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if tile.piece is not None :
                    tile.piece.draw(surface)

    def click(self, pos):

        x_pos = pos[0]
        y_pos = pos[1]

        self.deselect_if_selected()

        x, y = self.convert_coords_into_indecies(x_pos, y_pos)

        self.tiles[y][x].click()

        self.selection = pos

    def convert_coords_into_indecies(self, x_pos, y_pos):
        x = int(x_pos / settings.SQUARE_SIZE)
        y = int(y_pos / settings.SQUARE_SIZE)
        return x, y

    def deselect_if_selected(self):
        if self.selection is not None:
            self.deselect()

    def deselect(self):
        for row in self.tiles:
            for tile in row:
                tile.selected = False
                tile.highlighted = False

    def setup_standard(self):

        for tile in self.tiles[6]:
            new_pawn = Pawn(PieceSide.WHITE, tile.x, tile.y)
            tile.piece = new_pawn
            self.pieces.append(new_pawn)

        for tile in self.tiles[1]:
            new_pawn = Pawn(PieceSide.BLACK, tile.x, tile.y)
            tile.piece = new_pawn
            self.pieces.append(new_pawn)

        black_rook_one = Rook(PieceSide.BLACK, 0, 0)
        self.tiles[0][0].piece = black_rook_one
        self.pieces.append(black_rook_one)

        black_rook_two = Rook(PieceSide.BLACK, 7, 0)
        self.tiles[7][0].piece = black_rook_two
        self.pieces.append(black_rook_two)

        black_knight_one = Knight(PieceSide.BLACK, 1, 0)
        self.tiles[0][1].piece = black_knight_one
        self.pieces.append(black_knight_one)

        black_knight_two = Knight(PieceSide.BLACK, 6, 0)
        self.tiles[0][6].piece = black_knight_two
        self.pieces.append(black_knight_two)



