from board import Board
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King, PieceSide


class BoardSetter:

    def __init__(self):
        pass

    def setup(self, board):
        # Adds pawns

        for i in range(len(board.tiles[0])):
            white_pawn = Pawn(PieceSide.WHITE, i, 1)
            board.tiles[i][1].piece = white_pawn
            board.pieces.append(white_pawn)

            black_pawn = Pawn(PieceSide.BLACK, i, 6)
            board.tiles[i][6].piece = black_pawn
            board.pieces.append(black_pawn)

        # Black pieces

        black_rook_one = Rook(PieceSide.BLACK, 0, 7)
        board.tiles[0][7].piece = black_rook_one
        board.pieces.append(black_rook_one)

        black_rook_two = Rook(PieceSide.BLACK, 7, 7)
        board.tiles[7][7].piece = black_rook_two
        board.pieces.append(black_rook_two)

        black_knight_one = Knight(PieceSide.BLACK, 1, 7)
        board.tiles[1][7].piece = black_knight_one
        board.pieces.append(black_knight_one)

        black_knight_two = Knight(PieceSide.BLACK, 6, 7)
        board.tiles[6][7].piece = black_knight_two
        board.pieces.append(black_knight_two)

        black_bishop_one = Bishop(PieceSide.BLACK, 2, 7)
        board.tiles[2][7].piece = black_bishop_one
        board.pieces.append(black_bishop_one)

        black_bishop_two = Bishop(PieceSide.BLACK, 5, 7)
        board.tiles[5][7].piece = black_bishop_two
        board.pieces.append(black_bishop_two)

        black_king = King(PieceSide.BLACK, 3, 7)
        board.tiles[3][7].piece = black_king
        board.pieces.append(black_king)

        black_queen = Queen(PieceSide.BLACK, 4, 7)
        board.tiles[4][7].piece = black_queen
        board.pieces.append(black_queen)

        # White Pieces

        white_rook_one = Rook(PieceSide.WHITE, 0, 0)
        board.tiles[0][0].piece = white_rook_one
        board.pieces.append(white_rook_one)

        white_rook_two = Rook(PieceSide.WHITE, 7, 0)
        board.tiles[7][0].piece = white_rook_two
        board.pieces.append(white_rook_two)

        white_knight_one = Knight(PieceSide.WHITE, 1, 0)
        board.tiles[1][0].piece = white_knight_one
        board.pieces.append(white_knight_one)

        white_knight_two = Knight(PieceSide.WHITE, 6, 0)
        board.tiles[6][0].piece = white_knight_two
        board.pieces.append(white_knight_two)

        white_bishop_one = Bishop(PieceSide.WHITE, 2, 0)
        board.tiles[2][0].piece = white_bishop_one
        board.pieces.append(white_bishop_one)

        white_bishop_two = Bishop(PieceSide.WHITE, 5, 0)
        board.tiles[5][0].piece = white_bishop_two
        board.pieces.append(white_bishop_two)

        white_king = King(PieceSide.WHITE, 3, 0)
        board.tiles[3][0].piece = white_king
        board.pieces.append(white_king)

        white_queen = Queen(PieceSide.WHITE, 4, 0)
        board.tiles[4][0].piece = white_queen
        board.pieces.append(white_queen)
