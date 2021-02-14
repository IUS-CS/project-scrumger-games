# File: main.py
# Authors: John Cooke
# Since: 2/12/2021
# This file contains the main game loop and will initialize all the game systems
"""
This module will contain the main high level functions of the game, as well as the main game loop
"""
import logging
import os


import pygame

WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Froggerithm")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MOVEMENT_VELOCITY = 5

# Load title image
current_dir = os.path.dirname(os.path.abspath(__file__))
title_img = pygame.image.load(os.path.join(current_dir, "Assets", "logo.png"))


# Main game drawing function
def draw_window(title):
    """Draws the frame to be rendered"""
    WIN.fill(WHITE)
    WIN.blit(title_img, (title.x, title.y))
    pygame.display.update()

def log_game():
    """Initializes console for logging messages"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to The Froggerithm!")

def main():
    """Main game method containing the main game loop"""
    log_game()

    title = pygame.Rect(WIDTH / 2, HEIGHT / 2, title_img.get_width(), title_img.get_height())

    clock = pygame.time.Clock()
    run = True

    # Main game loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        # Input handling for movement
        keys_depressed = pygame.key.get_pressed()

        if keys_depressed[pygame.K_LEFT]:  # Left arrow key
            title.x -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_RIGHT]:  # Right arrow key
            title.x += MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_UP]:  # Up arrow key
            title.y -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_DOWN]:  # Down arrow key
            title.y += MOVEMENT_VELOCITY

        draw_window(title)


if __name__ == "__main__":
    main()
