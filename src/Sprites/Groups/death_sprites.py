import pygame.sprite


class DeathSprites(pygame.sprite.Group):
    """Pygame group class to be used for sprites that should kill the player on collision"""

    def __init__(self):
        pygame.sprite.Group.__init__(self)