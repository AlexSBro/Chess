from enum import Enum
import settings
import pygame


class PieceSide(Enum):
    WHITE = 0
    BLACK = 1


class Piece:

    piece_side = PieceSide.WHITE
    x = 0
    y = 0

    def __init__(self, piece_side, x, y):
        self.piece_side = piece_side
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (settings.SQUARE_SIZE*self.x, settings.SQUARE_SIZE*self.y))

    def highlight_possible_moves(self, tiles):
        pass


class Pawn(Piece):

    image = pygame.image

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_pawn.png")
        else:
            self.image = pygame.image.load("piece_images/black_pawn.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))

    def highlight_possible_moves(self, tiles):

        # Changes directions for black or white
        direction = 1
        if self.piece_side is PieceSide.WHITE:
            direction = -1

        # Highlights the move directly in front
        unoccupied = tiles[self.x][self.y + 1 * direction].highlight_if_unoccupied()

        # Checks for being on the first square and being able to move two ahead as long as it was not blocked before
        if unoccupied and (self.piece_side is PieceSide.WHITE and self.y is 6 or self.piece_side is PieceSide.BLACK and self.y is 1):
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
        pass


class Bishop(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_bishop.png")
        else:
            self.image = pygame.image.load("piece_images/black_bishop.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))


class Rook(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_rook.png")
        else:
            self.image = pygame.image.load("piece_images/black_rook.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))


class Queen(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_queen.png")
        else:
            self.image = pygame.image.load("piece_images/black_queen.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))


class King(Piece):

    def __init__(self, piece_side, x, y):
        Piece.__init__(self, piece_side, x, y)

        if piece_side == PieceSide.WHITE:
            self.image = pygame.image.load("piece_images/white_king.png")
        else:
            self.image = pygame.image.load("piece_images/black_king.png")

        self.image = pygame.transform.scale(self.image, (int(settings.SQUARE_SIZE), int(settings.SQUARE_SIZE)))



