from enum import Enum
from move import MoveType, PossibleMove
from piece_meta import PieceSide
import settings
import pygame
import abc


class PieceManager:

    white_king = None
    black_king = None

    living_pieces = []
    dead_pieces = []
    board = None
    last_piece_moved = None

    def __init__(self, board):
        self.board = board

    def select_piece(self, x, y, piece):
        piece.highlight_possible_moves(self.board.tiles, self)
        self.board.tiles[x][y].click()

    def check_for_piece(self, x, y):
        for piece in self.living_pieces:
            if piece.x is x and piece.y is y:
                return piece
        return None

    def check_occupied(self, x, y):
        return self.check_for_piece(x, y) is not None

    def occupied_by_friend(self, x, y, side):
        optional_piece = self.check_for_piece(x, y)
        if optional_piece is None:
            return False
        else:
            return optional_piece.piece_side is side

    def occupied_by_enemy(self, x, y, side):
        optional_piece = self.check_for_piece(x, y)
        if optional_piece is None:
            return False
        else:
            return optional_piece.piece_side is not side

    def can_move_to(self, x, y, side):
        optional_piece = self.check_for_piece(x, y)
        if optional_piece is None:
            return True
        else:
            return optional_piece.piece_side is not side

    # To use this method enter the players piece side.
    def under_attack(self, x, y, piece_side):
        for piece in self.living_pieces:
            if piece.piece_side is not piece_side:
                squares_under_attack = piece.get_possible_moves(self)
                for possible_move in squares_under_attack:
                    if possible_move.x is x and possible_move.y is y:
                        return True
        return False

    def draw(self, surface, perspective_white):
        for piece in self.living_pieces:
            piece.draw(surface, perspective_white)

    def king_in_check(self, piece_side):
        if piece_side is PieceSide.WHITE:
            return self.white_king.in_check(self)
        else:
            return self.black_king.in_check(self)


class Piece:

    moves = 0
    name = ""

    piece_side = PieceSide.WHITE
    x = 0
    y = 0

    def __init__(self, piece_side, x, y):
        self.piece_side = piece_side
        self.x = x
        self.y = y

    def draw(self, screen, perspective_white=True):
        y_adjusted = self.y
        if perspective_white:
            y_adjusted = abs(y_adjusted - 7)

        screen.blit(self.image, (settings.SQUARE_SIZE*self.x, settings.SQUARE_SIZE*y_adjusted))

    def highlight_possible_moves(self, tiles, piece_manager):
        possible_moves = self.get_possible_moves(piece_manager)
        for move in possible_moves:
            tiles[move.x][move.y].highlight(move.move_type)

    @abc.abstractmethod
    def get_possible_moves(self, piece_manager):
        possible_moves = []
        return possible_moves

    #This highlights if it is possible and returns if the piece should be able to keep moving.
    def highlight_if_can_move_to(self, x, y, piece_manager, possible_moves):
        optional_piece =  piece_manager.check_for_piece(x, y)
        if optional_piece is None:
            possible_moves.append(PossibleMove(x, y, MoveType.NORMAL))
            return True
        elif optional_piece.piece_side is not self.piece_side:
            possible_moves.append(PossibleMove(x, y, MoveType.NORMAL))
            return False
        elif optional_piece.piece_side is self.piece_side:
            return False


    def move(self, new_x, new_y, piece_manager, move_type=MoveType.NORMAL):
        self.x = new_x
        self.y = new_y

        self.moves += 1

        piece_manager.last_piece_moved = self

        return move_type

    def undo_move(self, old_x, old_y):
        self.x = old_x
        self.y = old_y

        self.moves -= 1

class Pawn(Piece):

    image = pygame.image

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side is PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_pawn.png")
        else:
            self.image = pygame.image.load("piece_images/black_pawn.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "Pawn"

    def get_possible_moves(self, piece_manager):

        possible_moves = []

        # Changes directions for black or white
        promotion_row = 0
        direction = -1
        if self.piece_side is PieceSide.WHITE:
            direction = 1
            promotion_row = 7

        move_type = MoveType.NORMAL
        if self.y + (1 * direction) is promotion_row:
            move_type = move_type.PROMOTION

        if not piece_manager.check_occupied(self.x, self.y + (1 * direction)):
            possible_moves.append(PossibleMove(self.x, self.y + (1 * direction), move_type))

        # Checks for diagonals and right with enemy pieces
        if self.x + 1 < 8 and piece_manager.occupied_by_enemy(self.x + 1, self.y + (1 * direction), self.piece_side):
            possible_moves.append(PossibleMove(self.x + 1, self.y + (1 * direction), move_type))

        # Checks for diagonals and left with enemy pieces
        if self.x - 1 > -1 and piece_manager.occupied_by_enemy(self.x - 1, self.y + 1 * direction, self.piece_side):
            possible_moves.append(PossibleMove(self.x - 1, self.y + (1 * direction), move_type))

        # Checks for being on the first square and being able to move two ahead as long as it was not blocked before
        if not piece_manager.check_occupied(self.x, self.y + (2 * direction)) and not piece_manager.check_occupied(self.x, self.y + (1 * direction)) and self.moves is 0:
            possible_moves.append(PossibleMove(self.x, self.y + 2 * direction, move_type))

        # Checks for diagonals and right with enemy pieces for en pessant
        if self.x + 1 < 8 and self.check_en_pessant(self.x + 1, self.y, self.piece_side, piece_manager):
            possible_moves.append(PossibleMove(self.x + 1, self.y + (1 * direction), MoveType.EN_PASSANT))

        # Checks for diagonals and left with enemy pieces for en pessant
        if self.x - 1 > -1 and  self.check_en_pessant(self.x - 1, self.y , self.piece_side, piece_manager):
            possible_moves.append(PossibleMove(self.x - 1, self.y + (1 * direction), MoveType.EN_PASSANT))

        return possible_moves

    def highlight_possible_moves(self, tiles, piece_manager):
        possible_moves = self.get_possible_moves(piece_manager)
        for move in possible_moves:
            tiles[move.x][move.y].highlight(move.move_type)


    def check_en_pessant(self, x, y, side, piece_manager):
        optional_piece = piece_manager.check_for_piece(x, y)
        if optional_piece is None:
            return False
        else:
            return optional_piece.piece_side is not side \
                   and isinstance(optional_piece, Pawn) \
                   and optional_piece is piece_manager.last_piece_moved \
                   and optional_piece.moves is 1


class Knight(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_knight.png")
        else:
            self.image = pygame.image.load("piece_images/black_knight.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "Knight"

    def get_possible_moves(self, piece_manager):
        possible_moves = []

        for i in range(1,3):
            for j in range(1,3):
                if i is not j:
                    if self.x + i < 8 and self.y + j < 8 and not piece_manager.occupied_by_friend(self.x + i, self.y + j, self.piece_side):
                        possible_moves.append(PossibleMove(self.x + i, self.y + j, MoveType.NORMAL))
                    if self.x - i >= 0 and self.y - j >= 0 and not piece_manager.occupied_by_friend(self.x - i, self.y - j, self.piece_side):
                        possible_moves.append(PossibleMove(self.x - i, self.y - j, MoveType.NORMAL))
                    if self.x + i < 8 and self.y - j >= 0 and not piece_manager.occupied_by_friend(self.x + i, self.y - j, self.piece_side):
                        possible_moves.append(PossibleMove(self.x + i,self.y - j , MoveType.NORMAL))
                    if self.x - i >= 0 and self.y + j < 8 and not piece_manager.occupied_by_friend(self.x - i, self.y + j, self.piece_side):
                        possible_moves.append(PossibleMove(self.x - i, self.y + j, MoveType.NORMAL))

        return possible_moves


class Bishop(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_bishop.png")
        else:
            self.image = pygame.image.load("piece_images/black_bishop.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "Bishop"


    def get_possible_moves(self, piece_manager):
        possible_moves = []

        move_up_right, move_down_right, move_down_left, move_up_left = (True, True, True, True)

        for i in range(1, 8):
            # Traverses up and right until hits piece
            if move_up_right and  self.y + i < 8 and self.x + i < 8:
                move_up_right = self.highlight_if_can_move_to(self.x + i, self.y + i, piece_manager, possible_moves)
            else:
                move_up_right = False

            # Traverses down and right until hits piece
            if move_down_right and  self.y - i >= 0 and self.x + i < 8:
                move_down_right = self.highlight_if_can_move_to(self.x + i, self.y - i, piece_manager, possible_moves)
            else:
                move_down_right = False
            # Traverses down and left until hits piece
            if move_down_left and self.y - i >= 0 and self.x - i >= 0:
                move_down_left = self.highlight_if_can_move_to(self.x - i, self.y - i, piece_manager, possible_moves)
            else:
                move_down_left = False
            # Traverses up and left until hits piece
            if move_up_left and self.x - i >= 0 and self.y + i < 8:
                move_up_left = self.highlight_if_can_move_to(self.x - i, self.y + i, piece_manager, possible_moves)
            else:
                move_up_left = False
            # Exits loop if no longer checking
            if not (move_up_right or move_down_right or move_down_left or move_up_left):
                break

        return possible_moves

class Rook(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_rook.png")
        else:
            self.image = pygame.image.load("piece_images/black_rook.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "Rook"

    def get_possible_moves(self, piece_manager):
        possible_moves = []

        move_up, move_down, move_right, move_left = (True, True, True, True)

        for i in range(1, 8):
            # Traverses up until hits piece
            if move_up and self.y + i < 8 and piece_manager.can_move_to(self.x, self.y + i, self.piece_side):
                move_up = self.highlight_if_can_move_to(self.x, self.y + i, piece_manager, possible_moves)
            else:
                move_up = False
            # Traverses down until hits piece
            if move_down and  self.y - i >= 0:
                move_down = self.highlight_if_can_move_to(self.x, self.y - i, piece_manager, possible_moves)
            else:
                move_down = False
            # Traverses right until hits piece
            if move_right and self.x + i < 8:
                move_right = self.highlight_if_can_move_to(self.x + i, self.y, piece_manager, possible_moves)
            else:
                move_right = False
            # Traverses left until hits piece
            if move_left and self.x - i >= 0:
                move_left = self.highlight_if_can_move_to(self.x - i, self.y, piece_manager, possible_moves)
            else:
                move_left = False
            # Exits loop if no longer checking
            if not (move_up or move_down or move_right or move_left):
                break

        return possible_moves



class Queen(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_queen.png")
        else:
            self.image = pygame.image.load("piece_images/black_queen.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "Queen"


    def get_possible_moves(self, piece_manager):
        possible_moves = []

        move_up_right, move_down_right, move_down_left, move_up_left, move_up, move_down, move_right, move_left = (True, True, True, True, True, True, True, True)

        for i in range(1, 8):
            # Traverses up until hits piece
            if move_up and self.y + i < 8 and piece_manager.can_move_to(self.x, self.y + i, self.piece_side):
                move_up = self.highlight_if_can_move_to(self.x, self.y + i, piece_manager, possible_moves)
            else:
                move_up = False
            # Traverses down until hits piece
            if move_down and  self.y - i >= 0:
                move_down = self.highlight_if_can_move_to(self.x, self.y - i, piece_manager, possible_moves)
            else:
                move_down = False
            # Traverses right until hits piece
            if move_right and self.x + i < 8:
                move_right = self.highlight_if_can_move_to(self.x + i, self.y, piece_manager, possible_moves)
            else:
                move_right = False
            # Traverses left until hits piece
            if move_left and self.x - i >= 0:
                move_left = self.highlight_if_can_move_to(self.x - i, self.y, piece_manager, possible_moves)
            else:
                move_left = False
            # Traverses up and right until hits piece
            if move_up_right and  self.y + i < 8 and self.x + i < 8:
                move_up_right = self.highlight_if_can_move_to(self.x + i, self.y + i, piece_manager, possible_moves)
            else:
                move_up_right = False

            # Traverses down and right until hits piece
            if move_down_right and  self.y - i >= 0 and self.x + i < 8:
                move_down_right = self.highlight_if_can_move_to(self.x + i, self.y - i, piece_manager, possible_moves)
            else:
                move_down_right = False
            # Traverses down and left until hits piece
            if move_down_left and self.y - i >= 0 and self.x - i >= 0:
                move_down_left = self.highlight_if_can_move_to(self.x - i, self.y - i, piece_manager, possible_moves)
            else:
                move_down_left = False
            # Traverses up and left until hits piece
            if move_up_left and self.x - i >= 0 and self.y + i < 8:
                move_up_left = self.highlight_if_can_move_to(self.x - i, self.y + i, piece_manager, possible_moves)
            else:
                move_up_left = False


            # Exits loop if no longer checking
            if not (move_up_right or move_down_right or move_down_left or move_up_left or move_up or move_down or move_right or move_left):
                break

        return possible_moves


class King(Piece):

    moved = False

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_king.png")
        else:
            self.image = pygame.image.load("piece_images/black_king.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))
        self.name = "King"

    def get_possible_moves(self, piece_manager):
        possible_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                translated_x, translated_y = self.x + i, self.y + j
                if 0 <= translated_x < 8 and 0 <= translated_y < 8 and not (i is 0 and j is 0):
                    self.highlight_if_can_move_to(translated_x, translated_y, piece_manager, possible_moves)

        if self.moves is 0:
            # Checks to castle on left
            if piece_manager.check_for_piece(self.x-2,self.y) is None and piece_manager.check_for_piece(self.x - 1,self.y) is None and type(piece_manager.check_for_piece(self.x - 3,self.y)) is Rook and piece_manager.check_for_piece(self.x - 3,self.y).moves is 0:
                possible_moves.append(PossibleMove(self.x - 2, self.y, MoveType.KING_SIDE_CASTLE))

            # Checks to castle on right
            if piece_manager.check_for_piece(self.x+3,self.y) is None and piece_manager.check_for_piece(self.x+2,self.y) is None and piece_manager.check_for_piece(self.x + 1,self.y) is None and type(piece_manager.check_for_piece(self.x + 4,self.y)) is Rook and piece_manager.check_for_piece(self.x + 4,self.y).moves is 0:
                possible_moves.append(self.x + 2, self.y, MoveType.QUEEN_SIDE_CASTLE)

        return possible_moves

    def highlight_possible_moves(self, tiles, piece_manager):
        possible_moves = self.get_possible_moves(piece_manager)
        for move in possible_moves:
            if not piece_manager.under_attack(move.x, move.y, self.piece_side):
                tiles[move.x][move.y].highlight(move.move_type)

    def in_check(self, piece_manager):
        return piece_manager.under_attack(self.x, self.y, self.piece_side)