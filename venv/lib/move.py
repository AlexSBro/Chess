import pieces

class Move:
    side = None
    piece = None
    from_x, from_y, to_x, to_y = (0, 0, 0, 0)

    def __init__(self, piece, from_x, from_y, to_x, to_y):
        self.from_x, self.from_y, self.to_x, self.to_y  = (from_x, from_y, to_x, to_y)
        self.piece = piece

class MoveManager:

    moves = []
    selected_piece = None
    piece_manager = None

    def __init__(self, piece_manager):
        self.piece_manager = piece_manager


    # def try_select(self, x, y, piece, board):
    #
    #     if self.selected_piece is not None:
    #         self.attempt_move(x, y, piece, board)
    #
    #     else:
    #         self.select_piece(x, y, piece, board)
    #
    #
    # def attempt_move(self, x, y, piece, board):
    #     if board.tiles[x][y].highlighted:
    #         piece.x = x
    #         piece.y = y
    #     else:
    #         self.selected_piece = None
    #         board.deselect()

    def click_tile(self, x, y):

        piece = self.piece_manager.check_for_piece(x, y)

        if piece is not None:
            self.select_or_take(piece, x, y)
        elif self.piece_manager.board.tiles[x][y].highlighted:
            self.move_piece(x, y)
        else:
            self.deselect()

    def select_or_take(self, piece, x, y):
        if self.selected_piece is None:
            self.selected_piece = piece
            self.piece_manager.select_piece(x, y, piece)
        elif self.selected_piece.piece_side is piece.piece_side:
            self.deselect()
        else:
            # take piece
            pass

    def move_piece(self, x, y):
        self.selected_piece.x = x
        self.selected_piece.y = y
        self.selected_piece.moved = True
        self.deselect()

    def deselect(self):
        self.selected_piece = None
        self.piece_manager.board.deselect()

    def attempt_move(self, piece, to_x, to_y):
        pass

    def get_last(self):
        pass

    def undo(self):
        pass
