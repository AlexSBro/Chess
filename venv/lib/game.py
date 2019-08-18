import pygame
import settings
import colors
import pieces

from board import Board

pygame.init()

game_display = pygame.display.set_mode((settings.BOARD_DIMEN, settings.BOARD_DIMEN))
pygame.display.set_caption(settings.NAME)
clock = pygame.time.Clock()

board = Board()
board.setup_standard()


def draw():

    board.draw(game_display)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            board.click(pos)
            print(event)

    draw()
    pygame.display.update()

    clock.tick(settings.FPS)

pygame.quit()
quit()