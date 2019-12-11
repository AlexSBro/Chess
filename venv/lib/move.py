import pieces
from piece_meta import PieceSide
from enum import Enum


class MoveType(Enum):
    NONE = 0
    NORMAL = 1
    KING_SIDE_CASTLE = 2
    QUEEN_SIDE_CASTLE = 3
    EN_PASSANT = 4
    PROMOTION = 5

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

        #Decided if selecting or moving an already selected piece
        if self.selected_piece is not None:
            selected_tile = self.piece_manager.board.tiles[x][y]
            #Case for valid move that is highlighted
            if selected_tile.move_type != MoveType.NONE:
                #Decides if it will be taking or just moving
                if piece is not None:
                    self.take(x, y)

                self.move_selected_piece(x, y, selected_tile.move_type)
                return True
            else:
                self.deselect()
        #Case for no current selection and attempts to select piece.
        elif piece is not None:
            #Ensures that you are selecting your own piece
            if piece.piece_side is self.turn:
                self.selected_piece = piece
                self.piece_manager.select_piece(x, y, piece)

        return False

    def deselect(self):
        self.selected_piece = None
        self.piece_manager.board.deselect()

    def move_selected_piece(self, x, y, move_type, piece_taken=None):

        print(move_type)

        # These select and move the correct rook if the piece is castling
        if move_type is MoveType.KING_SIDE_CASTLE:
            piece = self.piece_manager.check_for_piece(0, y)
            self.moves.append(
                Move(piece, None, piece.x, piece.y, 2, y, MoveType.NORMAL))
            piece.move(2, y, self.piece_manager)
        elif move_type is MoveType.QUEEN_SIDE_CASTLE:
            piece = self.piece_manager.check_for_piece(7, y)
            self.moves.append(
                Move(piece, None, piece.x, piece.y, 4, y, MoveType.NORMAL))
            piece.move(4, y, self.piece_manager)
        elif move_type is MoveType.EN_PASSANT:
            piece_taken = self.piece_manager.check_for_piece(x, self.selected_piece.y)
            self.take(x, self.selected_piece.y)

        #This is the code to move the expected piece as must be done for any case
        #This must be called first as it extracts the pieces original x,y
        self.moves.append(Move(self.selected_piece, piece_taken, self.selected_piece.x, self.selected_piece.y, x, y, move_type))
        #Code for actually moving the piece
        self.selected_piece.move(x, y, self.piece_manager)

        if move_type is MoveType.PROMOTION:
            new_queen = pieces.Queen(self.selected_piece.piece_side, self.selected_piece.x, self.selected_piece.y);
            self.piece_manager.living_pieces.remove(self.selected_piece)
            self.selected_piece = new_queen
            self.piece_manager.living_pieces.append(new_queen)

        self.deselect()

        self.toggle_turn()
        #This logs all of the moves in the game.
        self.print()

    def take(self, x, y):
        piece_taken = self.piece_manager.check_for_piece(x, y)
        self.piece_manager.living_pieces.remove(piece_taken)
        self.piece_manager.dead_pieces.append(piece_taken)

    def undo_if_moved(self):
        #Will only undo if there has actually been a move
        should_undo = len(self.moves) > 0

        if should_undo:
            self._undo()

        self.deselect()
        return should_undo

    def _undo(self):
        move_to_be_undone = self.moves[-1]

        piece_moved = move_to_be_undone.piece_moved
        piece_taken = move_to_be_undone.piece_taken

        #This must be called first as it re extracts the pawn that was promoted and puts it back into the living_pieces list
        self.revert_if_en_pessant(move_to_be_undone)

        piece_moved.undo_move(move_to_be_undone.from_x, move_to_be_undone.from_y)

        #This puts any pieces that were taken back into play
        self.restore_if_piece_taken(move_to_be_undone, piece_taken)

        #This recursive method calls this method again if the move was a castle so that both of the pieces will be moved back to where expected.
        if move_to_be_undone.move_type is MoveType.QUEEN_SIDE_CASTLE or move_to_be_undone.move_type is MoveType.KING_SIDE_CASTLE:
            self.undo()

        #This resets the piece managers last piece moved so that it can still decide if an en passant is necessary
        self.piece_manager.last_piece_moved = self.moves[-1].piece_moved

        self.toggle_turn()
        self.deselect()
        return True

    def restore_if_piece_taken(self, move_to_be_undone, piece_taken):
        if piece_taken is not None:
            self.piece_manager.living_pieces.append(piece_taken)
            self.piece_manager.dead_pieces.remove(piece_taken)
            if move_to_be_undone.move_type is MoveType.EN_PASSANT:
                piece_taken.y = move_to_be_undone.from_y
            else:
                piece_taken.y = move_to_be_undone.to_y
            piece_taken.x = move_to_be_undone.to_x
        self.moves.pop(-1)

    def revert_if_en_pessant(self, move_to_be_undone):
        # This logic pulls the pre existing pawn out of the MoveManager Move list so that expected behavior continues
        if move_to_be_undone.move_type is MoveType.PROMOTION:
            old_pawn = move_to_be_undone.piece_moved
            self.piece_manager.living_pieces.remove(self.piece_manager.check_for_piece(old_pawn.x, old_pawn.y))
            self.piece_manager.living_pieces.append(old_pawn)

    def toggle_turn(self):
        if self.turn is PieceSide.WHITE:
            self.turn = PieceSide.BLACK
        else:
            self.turn = PieceSide.WHITE

    def print(self):
        move = self.moves[len(self.moves) - 1]

        print(move.piece_moved.name, " (",move.from_x,",", move.from_y,") to (", move.to_x,",",  move.to_y,")")
