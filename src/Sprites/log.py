import pygame.sprite


class Log(pygame.sprite.Sprite):
    """
    Pygame sprite class representing a log floating in the river
    """

    def __init__(self, image, initial_x,  initial_y):
        """
        - :param image:
            An image asset representing the appearance the log will have
        - :param initial_x:
            The initial x position of the log. If set to -999, the log will spawn directly off the left side of the screen
        - :param initial_y:
            The initial y position of the log.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.y = initial_y
        self.set_x(initial_x)

    def set_x(self, x):
        """
        Helper function called by the constructor. Sets the x position of the log.

        - :param x:
            The initial x position of the log. If set to -999, the log will spawn directly off the left side of the screen.
        - :return:
            None
        """
        if x == -999:
            self.rect.x = -1 - self.image.get_width()
        else:
            self.rect.x = x
