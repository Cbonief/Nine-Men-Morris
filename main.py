import pygame
from jogo import Jogo

if __name__ == "__main__":
    janela = pygame.display.set_mode((600, 600))
    pygame.init()
    jogo = Jogo(janela)
    jogo.jogar()
