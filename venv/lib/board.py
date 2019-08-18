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
                pygame.draw.rect(surface, tile.get_color(), (tile.x*SQUARE_SIZE, tile.y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if tile.piece is not None :
                    tile.piece.draw(surface)

    def click(self, pos):

        x_pos = pos[0]
        y_pos = pos[1]

        self.deselect_if_selected()
        x, y = self.convert_coords_into_indecies(x_pos, y_pos)

        if self.selection is not None:
            self.move_piece(x, y)
        elif self.tiles[x][y].piece is not None:
            self.select_piece(x, y)

    def select_piece(self, x, y):
        self.tiles[x][y].piece.highlight_possible_moves(self.tiles)
        self.tiles[x][y].click()
        self.selection = self.tiles[x][y].piece

    def move_piece(self, x, y):
        if self.tiles[x][y].piece is None or not self.tiles[x][y].piece.piece_side == self.selection.piece_side:
            # Remove old selection
            self.tiles[self.selection.x][self.selection.y].piece = None
            # Remove piece on Square
            if not self.tiles[x][y].piece is None:
                self.pieces.remove(self.tiles[x][y].piece)
            # Set new coords
            self.selection.x = x
            self.selection.y = y
            # Add piece to new tile overriding old one if present
            self.tiles[x][y].piece = self.selection
            # Nullify board selection
        self.selection = None


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

        # Adds pawns

        for i in range(len(self.tiles[0])):
            white_pawn = Pawn(PieceSide.WHITE, i, 6)
            self.tiles[i][6].piece = white_pawn
            self.pieces.append(white_pawn)

            black_pawn = Pawn(PieceSide.BLACK, i, 1)
            self.tiles[i][1].piece = black_pawn
            self.pieces.append(black_pawn)

        # Black pieces

        black_rook_one = Rook(PieceSide.BLACK, 0, 0)
        self.tiles[0][0].piece = black_rook_one
        self.pieces.append(black_rook_one)

        black_rook_two = Rook(PieceSide.BLACK, 7, 0)
        self.tiles[7][0].piece = black_rook_two
        self.pieces.append(black_rook_two)

        black_knight_one = Knight(PieceSide.BLACK, 1, 0)
        self.tiles[1][0].piece = black_knight_one
        self.pieces.append(black_knight_one)

        black_knight_two = Knight(PieceSide.BLACK, 6, 0)
        self.tiles[6][0].piece = black_knight_two
        self.pieces.append(black_knight_two)

        black_bishop_one = Bishop(PieceSide.BLACK, 2, 0)
        self.tiles[2][0].piece = black_bishop_one
        self.pieces.append(black_bishop_one)

        black_bishop_two = Bishop(PieceSide.BLACK, 5, 0)
        self.tiles[5][0].piece = black_bishop_two
        self.pieces.append(black_bishop_two)

        black_king = King(PieceSide.BLACK, 3, 0)
        self.tiles[3][0].piece = black_king
        self.pieces.append(black_king)

        black_queen = Queen(PieceSide.BLACK, 4, 0)
        self.tiles[4][0].piece = black_queen
        self.pieces.append(black_queen)

        # White Pieces

        white_rook_one = Rook(PieceSide.WHITE, 0, 7)
        self.tiles[0][7].piece = white_rook_one
        self.pieces.append(white_rook_one)

        white_rook_two = Rook(PieceSide.WHITE, 7, 7)
        self.tiles[7][7].piece = white_rook_two
        self.pieces.append(white_rook_two)

        white_knight_one = Knight(PieceSide.WHITE, 1, 7)
        self.tiles[1][7].piece = white_knight_one
        self.pieces.append(white_knight_one)

        white_knight_two = Knight(PieceSide.WHITE, 6, 7)
        self.tiles[6][7].piece = white_knight_two
        self.pieces.append(white_knight_two)

        white_bishop_one = Bishop(PieceSide.WHITE, 2, 7)
        self.tiles[2][7].piece = white_bishop_one
        self.pieces.append(white_bishop_one)

        white_bishop_two = Bishop(PieceSide.WHITE, 5, 7)
        self.tiles[5][7].piece = white_bishop_two
        self.pieces.append(white_bishop_two)

        white_king = King(PieceSide.WHITE, 3, 7)
        self.tiles[3][7].piece = white_king
        self.pieces.append(white_king)

        white_queen = Queen(PieceSide.WHITE, 4, 7)
        self.tiles[4][7].piece = white_queen
        self.pieces.append(white_queen)
