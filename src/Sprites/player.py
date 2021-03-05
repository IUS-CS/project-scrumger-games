import pygame.sprite
import pygame.surface


class Player(pygame.sprite.Sprite):
    """Pygame sprite class representing the player"""

    def __init__(self, images, win: pygame.surface.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = win.get_width() / 2
        self.rect.y = win.get_height() - self.rect.height - 11
        self.index = 0
        self.image = images[self.index]
        self.direction = "up"
        self.score = 0
        self.farthest_distance = 900

