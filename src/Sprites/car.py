import pygame.sprite
import pygame.surface


class Car(pygame.sprite.Sprite):
    """
    Pygame sprite class representing a car.
    """

    def __init__(self, image, x, y, win: pygame.surface.Surface):
        """
        - :param image:
            An image asset that will become the sprite's visual representation
        - :param x:
            An int representing the x position the car should start at
        - :param y:
            An int representing the y position the car should start at
        :param win:
            A pygame Surface object onto which the car will be drawn
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

