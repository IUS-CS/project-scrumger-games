import pygame.sprite


class WaterSprite(pygame.sprite.Sprite):
    """
    Pygame sprite class for a water sprite used for killing the player when they fall into the water.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([820, 400])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 25


class RiverEdge(pygame.sprite.Sprite):
    """
    Pygame sprite class used to kill the player if they ride off the screen in the river.
    """

    def __init__(self, side):
        """
        - :param side:
            A string containing which side of the river to place the sprite. Should be "left" or "right". Anything else
            will cause unexpected behavior.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 400])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 25

        if side == "left":
            self.rect.x = -60
        else:
            self.rect.x = 860
