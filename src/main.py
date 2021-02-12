import pygame
import os
import logging
from testfixtures import LogCapture

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
    WIN.fill(WHITE)
    WIN.blit(title_img, (title.x, title.y))
    pygame.display.update()

def log_game():
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to The Froggerithm!")

def main():

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

    pygame.quit()


if __name__ == "__main__":
    main()