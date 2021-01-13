import pygame

from game import Game

if __name__ == "__main__":
    window = pygame.display.set_mode((600, 600))
    pygame.init()
    game = Game(window)
    game.run()
