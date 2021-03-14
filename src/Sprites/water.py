import pygame.sprite


class WaterSprite(pygame.sprite.Sprite):
    """Pygame sprite class for water sprites used for killing the player"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([820, 400])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 25



