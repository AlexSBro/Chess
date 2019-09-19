from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, PieceSide, PieceManager


class BoardSetter:

    def __init__(self):
        pass

    def setup(self, piece_manager):
        # Adds pawns

        for i in range(8):
            white_pawn = Pawn(PieceSide.WHITE, i, 1)
            piece_manager.pieces.append(white_pawn)

            black_pawn = Pawn(PieceSide.BLACK, i, 6)
            piece_manager.pieces.append(black_pawn)

        # Black pieces

        black_rook_one = Rook(PieceSide.BLACK, 0, 7)
        piece_manager.pieces.append(black_rook_one)

        black_rook_two = Rook(PieceSide.BLACK, 7, 7)
        piece_manager.pieces.append(black_rook_two)

        black_knight_one = Knight(PieceSide.BLACK, 1, 7)
        piece_manager.pieces.append(black_knight_one)

        black_knight_two = Knight(PieceSide.BLACK, 6, 7)
        piece_manager.pieces.append(black_knight_two)

        black_bishop_one = Bishop(PieceSide.BLACK, 2, 7)
        piece_manager.pieces.append(black_bishop_one)

        black_bishop_two = Bishop(PieceSide.BLACK, 5, 7)
        piece_manager.pieces.append(black_bishop_two)

        black_king = King(PieceSide.BLACK, 3, 7)
        piece_manager.pieces.append(black_king)

        black_queen = Queen(PieceSide.BLACK, 4, 7)
        piece_manager.pieces.append(black_queen)

        # White Pieces

        white_rook_one = Rook(PieceSide.WHITE, 0, 0)
        piece_manager.pieces.append(white_rook_one)

        white_rook_two = Rook(PieceSide.WHITE, 7, 0)
        piece_manager.pieces.append(white_rook_two)

        white_knight_one = Knight(PieceSide.WHITE, 1, 0)
        piece_manager.pieces.append(white_knight_one)

        white_knight_two = Knight(PieceSide.WHITE, 6, 0)
        piece_manager.pieces.append(white_knight_two)

        white_bishop_one = Bishop(PieceSide.WHITE, 2, 0)
        piece_manager.pieces.append(white_bishop_one)

        white_bishop_two = Bishop(PieceSide.WHITE, 5, 0)
        piece_manager.pieces.append(white_bishop_two)

        white_king = King(PieceSide.WHITE, 3, 0)
        piece_manager.pieces.append(white_king)

        white_queen = Queen(PieceSide.WHITE, 4, 0)
        piece_manager.pieces.append(white_queen)
