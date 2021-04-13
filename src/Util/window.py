import pygame.display
import pygame.sprite


class Window:
    """Static window class containing information about the game window."""
    WIDTH = 820
    HEIGHT = 876
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    FINAL_SCORE = 0
    HIGHEST_SCORE = 0
    GREATEST_LIVES = 0
