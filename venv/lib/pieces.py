from enum import Enum
import settings
import pygame


class PieceSide(Enum):
    WHITE = 0
    BLACK = 1


class Piece:

    moved = False

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

    def highlight_possible_moves(self, tiles):
        pass

    def move(self, new_x, new_y, tiles):
        self.x = new_x
        self.y = new_y

        self.moved = True

class Pawn(Piece):

    image = pygame.image

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side is PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_pawn.png")
        else:
            self.image = pygame.image.load("piece_images/black_pawn.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))

    def highlight_possible_moves(self, tiles):

        # Changes directions for black or white
        direction = -1
        if self.piece_side is PieceSide.WHITE:
            direction = 1

        # Highlights the move directly in front
        unoccupied = tiles[self.x][self.y + 1 * direction].highlight_if_unoccupied()

        # Checks for being on the first square and being able to move two ahead as long as it was not blocked before
        if unoccupied and not self.moved:
            tiles[self.x][self.y + 2 * direction].highlight_if_unoccupied()

        # Checks for diagonals and right with enemy pieces
        if self.x + 1 < 8 and tiles[self.x + 1][self.y + 1 * direction].piece is not None and tiles[self.x + 1][self.y + 1 * direction].piece.piece_side is not self.piece_side:
            tiles[self.x + 1][self.y + 1 * direction].highlight_if_unoccupied_by_friend(self.piece_side)
        # Checks for diagonals and left with enemy pieces
        if self.x - 1 > -1 and tiles[self.x - 1][self.y + 1 * direction].piece is not None and tiles[self.x - 1][self.y + 1 * direction].piece.piece_side is not self.piece_side:
            tiles[self.x - 1][self.y + 1 * direction].highlight_if_unoccupied_by_friend(self.piece_side)


class Knight(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_knight.png")
        else:
            self.image = pygame.image.load("piece_images/black_knight.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))

    def highlight_possible_moves(self, tiles):

        for i in range(1,3):
            for j in range(1,3):
                if i is not j:
                    if self.x + i < 8 and self.y + j < 8:
                        tiles[self.x + i][self.y + j].highlight_if_unoccupied_by_friend(self.piece_side)
                    if self.x - i >= 0 and self.y - j >= 0:
                        tiles[self.x - i][self.y - j].highlight_if_unoccupied_by_friend(self.piece_side)
                    if self.x + i < 8 and self.y - j >= 0:
                        tiles[self.x + i][self.y - j].highlight_if_unoccupied_by_friend(self.piece_side)
                    if self.x - i >= 0 and self.y + j < 8:
                        tiles[self.x - i][self.y + j].highlight_if_unoccupied_by_friend(self.piece_side)


class Bishop(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_bishop.png")
        else:
            self.image = pygame.image.load("piece_images/black_bishop.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))


    def highlight_possible_moves(self, tiles):
        move_up_right, move_down_right, move_down_left, move_up_left = (True, True, True, True)

        for i in range(1, 8):
            # Traverses up and right until hits piece
            if self.y + i < 8 and self.x + i < 8 and move_up_right:
                move_up_right = tiles[self.x + i][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up_right = False
            # Traverses down and right until hits piece
            if self.y - i >= 0 and self.x + i < 8 and move_down_right:
                move_down_right = tiles[self.x + i][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down_right = False
            # Traverses down and left until hits piece
            if self.y - i >= 0 and self.x - i >= 0 and move_down_left:
                move_down_left = tiles[self.x - i][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down_left = False
            # Traverses up and left until hits piece
            if self.x - i >= 0 and self.y + i < 8 and move_up_left:
                move_up_left = tiles[self.x - i][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up_left = False
            # Exits loop if no longer checking
            if not (move_up_right or move_down_right or move_down_left or move_up_left):
                break

class Rook(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_rook.png")
        else:
            self.image = pygame.image.load("piece_images/black_rook.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))

    def highlight_possible_moves(self, tiles):
        move_up, move_down, move_right, move_left = (True, True, True, True)

        for i in range(1, 8):
            # Traverses up until hits piece
            if self.y + i < 8 and move_up:
                move_up = tiles[self.x][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up = False
            # Traverses down until hits piece
            if self.y - i >= 0 and move_down:
                move_down = tiles[self.x][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down = False
            # Traverses right until hits piece
            if self.x + i < 8 and move_right:
                move_right = tiles[self.x + i][self.y].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_right = False
            # Traverses left until hits piece
            if self.x - i >= 0 and move_left:
                move_left = tiles[self.x - i][self.y].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_left = False
            # Exits loop if no longer checking
            if not (move_up or move_down or move_right or move_left):
                break



class Queen(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_queen.png")
        else:
            self.image = pygame.image.load("piece_images/black_queen.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))


    def highlight_possible_moves(self, tiles):

        move_up_right, move_down_right, move_down_left, move_up_left, move_up, move_down, move_right, move_left = (True, True, True, True, True, True, True, True)

        for i in range(1, 8):
            # Traverses up until hits piece
            if self.y + i < 8 and move_up:
                move_up = tiles[self.x][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up = False
            # Traverses down until hits piece
            if self.y - i >= 0 and move_down:
                move_down = tiles[self.x][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down = False
            # Traverses right until hits piece
            if self.x + i < 8 and move_right:
                move_right = tiles[self.x + i][self.y].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_right = False
            # Traverses left until hits piece
            if self.x - i >= 0 and move_left:
                move_left = tiles[self.x - i][self.y].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_left = False
            # Traverses up and right until hits piece
            if self.y + i < 8 and self.x + i < 8 and move_up_right:
                move_up_right = tiles[self.x + i][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up_right = False
            # Traverses down and right until hits piece
            if self.y - i >= 0 and self.x + i < 8 and move_down_right:
                move_down_right = tiles[self.x + i][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down_right = False
            # Traverses down and left until hits piece
            if self.y - i >= 0 and self.x - i >= 0 and move_down_left:
                move_down_left = tiles[self.x - i][self.y - i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_down_left = False
            # Traverses up and left until hits piece
            if self.x - i >= 0 and self.y + i < 8 and move_up_left:
                move_up_left = tiles[self.x - i][self.y + i].highlight_if_unoccupied_by_friend(self.piece_side)
            else:
                move_up_left = False
            # Exits loop if no longer checking
            if not (move_up_right or move_down_right or move_down_left or move_up_left or move_up or move_down or move_right or move_left):
                break


class King(Piece):

    moved = False

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_king.png")
        else:
            self.image = pygame.image.load("piece_images/black_king.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))

    def highlight_possible_moves(self, tiles):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= self.x + i < 8 and 0 <= self.y + j < 8 and not (i is 0 and j is 0):
                    tiles[self.x + i][self.y + j].highlight_if_unoccupied_by_friend(self.piece_side)

        if not self.moved:
            # Checks to castle on left
            if tiles[self.x-2][self.y].piece is None and tiles[self.x - 1][self.y].piece is None and type(tiles[self.x - 3][self.y].piece) is Rook and not tiles[self.x - 3][self.y].piece.moved:
                tiles[self.x - 2][self.y].highlighted = True
            # Checks to castle on right
            if tiles[self.x+3][self.y].piece is None and tiles[self.x+2][self.y].piece is None and tiles[self.x + 1][self.y].piece is None and type(tiles[self.x + 4][self.y].piece) is Rook and not tiles[self.x + 4][self.y].piece.moved:
                tiles[self.x + 2][self.y].highlighted = True

    def move(self, new_x, new_y, tiles):
        # Checks if castling to the right and moves the rook if doing so
        if new_x is self.x - 2:
            rook = tiles[0][self.y].piece
            rook.move(self.x-1, self.y, tiles)
            tiles[self.x-1][self.y].piece = rook
            tiles[0][self.y].piece = None
        # Checks if castling to the left and moves the rook if doing so
        if new_x is self.x + 2:
            rook = tiles[7][self.y].piece
            rook.move(self.x + 1, self.y, tiles)
            tiles[self.x + 1][self.y].piece = rook
            tiles[7][self.y].piece = None
        # Moves itself after the rook
        Piece.move(self, new_x, new_y, tiles)
