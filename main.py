import pygame
from game import Game

if __name__ == "__main__":
    janela = pygame.display.set_mode((600, 600))
    pygame.init()
    jogo = Game(janela)
    jogo.run()
