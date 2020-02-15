"""Implementation of main to run a game as a player
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   20.01.2020
"""

import pygame
import pygame_gui

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

    manager = pygame_gui.UIManager((800, 600))

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(backgound, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()

    """
    ********************************************************************
    """
    #TODO