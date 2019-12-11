import colors
from enum import Enum
from move import MoveType


class TileSide(Enum):
    LIGHT = 0
    DARK = 1


class Tile:

    x,y = 0,0

    selected = False
    tile_side = TileSide.LIGHT
    move_type = MoveType.NONE

    def __init__(self, x, y, tile_side):
        self.x = x
        self.y = y
        self.tile_side = tile_side

    def get_color(self):

        if self.selected:
            return colors.SELECTION

        # Return Light
        if self.tile_side == TileSide.LIGHT:
            if self.move_type != MoveType.NONE:
                return colors.LIGHT_TILE_HIGHLIGHT
            else:
                return colors.LIGHT_TILE
        # Return Dark
        else:
            if self.move_type != MoveType.NONE:
                return colors.DARK_TILE_HIGHLIGHT
            else:
                return colors.DARK_TILE

    def click(self):
        self.selected = True

    def highlight(self, move_type=MoveType.NORMAL):
        self.move_type = move_type

    def un_highlight(self):
        self.move_type = MoveType.NONE

