import colors
from enum import Enum


class TileSide(Enum):
    LIGHT = 0
    DARK = 1


class Tile:

    x,y = 0,0

    selected = False
    highlighted = False
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

