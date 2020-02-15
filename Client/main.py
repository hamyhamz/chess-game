"""Implementation of main to run a game as a player
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   20.01.2020
"""

import pygame

if __name__ == '__main__':
    print("Hello everyone!")

    """
    ********************************************************************
        Code taken from https://pygame-gui.readthedocs.io/en/latest/quick_start.html
        As a quick demonstration of initial window creation in pygame
    """
    pygame.init()

    pygame.display.set_caption('Chess Game v.0')
    window_surface = pygame.display.set_mode((800, 600))

    backgound = pygame.Surface((800, 600))
    backgound.fill(pygame.Color('#000000'))

    is_running = True

    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(backgound, (0, 0))

        pygame.display.update()

    """
    ********************************************************************
    """
    #TODO