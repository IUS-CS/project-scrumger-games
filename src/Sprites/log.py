import pygame.sprite
from Util.window import Window


class Log(pygame.sprite.Sprite):
    """Pygame sprite class representing a log floating in the river"""

    def __init__(self, image, initial_x,  initial_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.y = initial_y
        self.set_x(initial_x)
        self.add(Window.SPRITE_LIST)


    def set_x(self, x):
        if x == -999:
            self.rect.x = -1 - self.image.get_width()
        else:
            self.rect.x = x