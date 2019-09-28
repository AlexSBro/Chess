import pygame
import settings
import colors
import pieces
import move
import board_setter

from board import Board

pygame.init()

game_display = pygame.display.set_mode((settings.BOARD_DIMEN, settings.BOARD_DIMEN))
pygame.display.set_caption(settings.NAME)
clock = pygame.time.Clock()

board = Board()
piece_manager = pieces.PieceManager(board)
move_manager = move.MoveManager(piece_manager)

board_setup = board_setter.BoardSetter()
board_setup.setup(piece_manager)

def draw():

    board.draw(game_display)
    piece_manager.draw(game_display, board.perspective_white)


running = True

while running:

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type is pygame.MOUSEBUTTONUP:

            pos = pygame.mouse.get_pos()

            x, y = board.click(pos)

            if move_manager.click_tile(x, y):
                board.perspective_white = not board.perspective_white

        if event.type is pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.perspective_white = not board.perspective_white
            if event.key == pygame.K_u:
                move_manager.undo()
                board.perspective_white = not board.perspective_white

    draw()
    pygame.display.update()

    clock.tick(settings.FPS)

pygame.quit()
quit()
