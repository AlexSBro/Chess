import colors
from enum import Enum


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

        # Return Light
        if self.tile_side == TileSide.LIGHT:
            if self.highlighted:
                return colors.LIGHT_TILE_HIGHLIGHT
            else:
                return colors.LIGHT_TILE
        # Return Dark
        else:
            if self.highlighted:
                return colors.DARK_TILE_HIGHLIGHT
            else:
                return colors.DARK_TILE

    def click(self):
        self.selected = True

    def highlight_if_unoccupied_by_friend(self, side):

        if self.piece is not None:
            if self.piece.piece_side is side:
                self.highlighted = False
            else:
                self.highlighted = True
            return False

        else:
            self.highlighted = True
            return True


    def highlight_if_unoccupied(self):

        if self.piece is not None:
            self.highlighted = False
            return False

        else:
            self.highlighted = True
            return True

