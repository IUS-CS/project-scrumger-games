import pygame.sprite


class Riverbank(pygame.sprite.Sprite):
    """
    Pygame sprite class for riverbank sprites used for killing the player
    """

    # Constructor should be passed an int to indicate which position the sprite should go in
    def __init__(self, pos):
        """
        - :param pos:
            An int representing the "index" of the riverbank. Should be 0-5, with 0 representing the left-most riverbank
            and 5 representing the right-most bank.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([70, 50])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 40
        self.set_pos(pos)

    def set_pos(self, pos):
        """
        Helper function called by constructor. Takes the position argument passed to the constructor and places the nest
        in the proper slot.

        - :param pos:
            An int representing the "index" of the riverbank. Should be 0-5, with 1 representing the left-most riverbank
            and 5 representing the right-most bank.
        - :return:
            None
        """
        if pos == 0:
            self.rect.x = -15
        elif pos == 1:
            self.rect.x = 148

        elif pos == 2:
            self.rect.x = 310

        elif pos == 3:
            self.rect.x = 470

        elif pos == 4:
            self.rect.x = 630

        elif pos == 5:
            self.rect.x = 789
