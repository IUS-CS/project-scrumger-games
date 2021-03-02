import pygame.sprite
import pygame.surface


class Player(pygame.sprite.Sprite):
    """Pygame sprite class representing the player"""

    def __init__(self, image, win: pygame.surface.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = win.get_width() / 2
        self.rect.y = win.get_height() - self.rect.height - 9