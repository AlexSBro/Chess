import pygame
import settings
import colors
import pieces
import board_setter

from board import Board

pygame.init()

game_display = pygame.display.set_mode((settings.BOARD_DIMEN, settings.BOARD_DIMEN))
pygame.display.set_caption(settings.NAME)
clock = pygame.time.Clock()

board = Board()
board_setup = board_setter.BoardSetter()
board_setup.setup(board)

def draw():

    board.draw(game_display)


running = True

while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type is pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            board.click(pos)
        if event.type is pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.perspective_white = not board.perspective_white

    draw()
    pygame.display.update()

    clock.tick(settings.FPS)

pygame.quit()
quit()
