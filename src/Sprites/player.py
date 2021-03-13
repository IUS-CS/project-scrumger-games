import pygame.sprite
import pygame.surface
from Util.window import Window
from Util.utilities import quit_game


class Player(pygame.sprite.Sprite):
    """Pygame sprite class representing the player"""

    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = images[self.index]
        self.direction = "up"
        self.score = 0
        self.farthest_distance = 900
        self.lives_left = 6

    def nest(self):
        self.return_home()
        self.farthest_distance = 900
        self.score += 50

    def win_game(self):
        self.score += 1000
        quit_game(self)

    def kill(self):
        self.return_home()
        self.lives_left -= 1

        if self.lives_left < 0:
            quit_game(self)

    def return_home(self):
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = self.images[self.index]
        self.direction = "up"
