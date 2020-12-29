import pygame
from trilha import Jogo

if __name__ == "__main__":
    win = pygame.display.set_mode((600, 600))
    pygame.init()
    jogo = Jogo(win)
    jogo.run()
