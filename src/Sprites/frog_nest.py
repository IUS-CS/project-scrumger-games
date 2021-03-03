import pygame.sprite


class FrogNest(pygame.sprite.Sprite):
    """Pygame sprite class for frog nests used for checking the win condition"""

    # Constructor should be passed an int to indicate which nest position the sprite should go in
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([74, 50])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 40
        self.set_pos(pos)

    def set_pos(self, pos):
        if pos == 1:
            self.rect.x = 67

        elif pos == 2:
            self.rect.x = 227

        elif pos == 3:
            self.rect.x = 387

        elif pos == 4:
            self.rect.x = 547

        else:
            self.rect.x = 707