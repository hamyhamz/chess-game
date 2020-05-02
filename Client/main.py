"""Implementation of main to run a game as a client side player
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   20.01.2020
"""

import pygame
import pygame_gui

if __name__ == '__main__':

    # Initialize the pygame framework
    pygame.init()

    # Cteate the main game screen
    screen = pygame.display.set_mode((800, 600))

    # Game state variable
    running = True

    # Game loop
    while running:
        for event in pygame.event.get():

            # React on quit event
            if event.type == pygame.QUIT:
                running = False
    #TODO