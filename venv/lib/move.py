import pieces
from piece_meta import PieceSide
from enum import Enum


class MoveType(Enum):
    NORMAL = 0
    KING_SIDE_CASTLE = 1
    QUEEN_SIDE_CASTLE = 2


class Move:

    move_type = MoveType.NORMAL

    piece_moved = None
    piece_taken = None

    from_x, from_y, to_x, to_y = (0, 0, 0, 0)

    def __init__(self, piece_moved, piece_taken, from_x, from_y, to_x, to_y, move_type=MoveType.NORMAL):
        self.from_x, self.from_y, self.to_x, self.to_y  = (from_x, from_y, to_x, to_y)
        self.piece_moved = piece_moved
        self.piece_taken = piece_taken
        self.move_type = move_type


class MoveManager:

    turn = PieceSide.WHITE

    moves = []
    selected_piece = None
    piece_manager = None

    def __init__(self, piece_manager):
        self.piece_manager = piece_manager

    def click_tile(self, x, y):

        piece = self.piece_manager.check_for_piece(x, y)

        if self.selected_piece is not None:
            if self.piece_manager.board.tiles[x][y].highlighted:
                if piece is not None:
                    self.take(x, y)
                else:
                    self.move_selected_piece(x, y)
                return True
            else:
                self.deselect()

        elif piece is not None:
            if piece.piece_side is self.turn:
                self.selected_piece = piece
                self.piece_manager.select_piece(x, y, piece)

        return False

    def deselect(self):
        self.selected_piece = None
        self.piece_manager.board.deselect()

    def move_selected_piece(self, x, y, piece_taken=None):
        #This must be called first as it extracts the pieces original x,y
        self.moves.append(Move(self.selected_piece, piece_taken, self.selected_piece.x, self.selected_piece.y, x, y))

        self.selected_piece.move(x, y, self.piece_manager)

        self.deselect()

        self.toggle_turn()
        self.print()

    def take(self, x, y):
        piece_taken = self.piece_manager.check_for_piece(x, y)
        self.piece_manager.living_pieces.remove(piece_taken)
        self.piece_manager.dead_pieces.append(piece_taken)
        self.move_selected_piece(x, y, piece_taken)

    def get_last(self):
        pass

    def undo(self):
        if len(self.moves) > 0:
            piece_moved = self.moves[-1].piece_moved
            piece_taken = self.moves[-1].piece_taken

            piece_moved.undo_move(self.moves[-1].from_x, self.moves[-1].from_y)
            if piece_taken is not None:
                self.piece_manager.living_pieces.append(piece_taken)
                self.piece_manager.dead_pieces.remove(piece_taken)
                piece_taken.x = self.moves[-1].to_x
                piece_taken.y = self.moves[-1].to_y
            self.moves.pop(-1)

        self.toggle_turn()
        self.deselect()

    def toggle_turn(self):
        if self.turn is PieceSide.WHITE:
            self.turn = PieceSide.BLACK
        else:
            self.turn = PieceSide.WHITE

    def print(self):
        move = self.moves[len(self.moves) - 1]

        print(move.piece_moved.name, " (",move.from_x,",", move.from_y,") to (", move.to_x,",",  move.to_y,")")
