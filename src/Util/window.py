import pygame.display


class Window:

    WIDTH = 820
    HEIGHT = 876
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    FINAL_SCORE = 0
    TIMER = 30
    TIMER_TEXT = str(TIMER).rjust(5)
