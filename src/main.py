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

WIDTH, HEIGHT = 800, 880
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Froggerithm")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MOVEMENT_VELOCITY = 5
current_dir = os.path.dirname(os.path.abspath(__file__))


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


def is_colliding(rect1, rect2):
    return rect1.colliderect(rect2)


# Load images
background_image = pygame.image.load(os.path.join(current_dir, "Assets", "background.png"))
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

frog_image = pygame.image.load(os.path.join(current_dir, "Assets", "frog.png"))
frog = scale_image(frog_image)

car_image = pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png"))
car_scaled = scale_image(car_image)


# Main game drawing function
def draw_window(player):
    """Draws the frame to be rendered"""
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))
    WIN.blit(frog, (player.x, player.y))
    pygame.display.update()

def log_game():
    """Initializes console for logging messages"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to The Froggerithm!")

def main():
    """Main game method containing the main game loop"""
    log_game()

    player = pygame.Rect(WIDTH / 2, HEIGHT - frog.get_width(), frog.get_width(), frog.get_height())
    car = pygame.Rect(WIDTH / 2, HEIGHT - car_scaled.get_width(), car_scaled.get_width(), car_scaled.get_height())

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

        if keys_depressed[pygame.K_LEFT] or keys_depressed[pygame.K_a]:  # Left arrow key or a
            player.x -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_RIGHT] or keys_depressed[pygame.K_d]:  # Right arrow key or d
            player.x += MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_UP] or keys_depressed[pygame.K_w]:  # Up arrow key or w
            player.y -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_DOWN] or keys_depressed[pygame.K_s]:  # Down arrow key or s
            player.y += MOVEMENT_VELOCITY

        if is_colliding(player, car):
            print("COLLISION")

        draw_window(player)


if __name__ == "__main__":
    main()
