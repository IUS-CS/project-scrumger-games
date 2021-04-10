import pygame.sprite
import pygame.surface


class Car(pygame.sprite.Sprite):
    """Pygame sprite class representing a car"""

    def __init__(self, image, x, y, win: pygame.surface.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

