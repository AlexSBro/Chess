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
    board = None
    pieces = None

    def attempt_move(self, piece, to_x, to_y):
        pass

    def get_last(self):
        pass

    def undo(self):
        pass
