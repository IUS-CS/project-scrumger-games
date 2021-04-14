import pygame.sprite
from Util.asset_dictionary import AssetDictionary


class FrogNest(pygame.sprite.Sprite):
    """
    Pygame sprite class for frog nests used for checking the win condition.
    """

    # Constructor should be passed an int to indicate which nest position the sprite should go in
    def __init__(self, pos):
        """
        - :param pos:
            An int representing the "index" of the nest. Should be 1-5, with 1 representing the left-most nest and 5 representing the right-most nest.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([70, 50])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.y = 40
        self.set_pos(pos)

    def set_pos(self, pos):
        """
        Helper method called by the constructor. Takes the position argument passed to the constructor and places the nest in the proper slot.

        - :param pos:
            An int representing the "index" of the nest. Should be 1-5, with 1 representing the left-most nest and 5 representing the right-most nest.
        - :return:
            None
        """
        if pos == 1:
            self.rect.x = 67

        elif pos == 2:
            self.rect.x = 230

        elif pos == 3:
            self.rect.x = 390

        elif pos == 4:
            self.rect.x = 550

        else:
            self.rect.x = 710

    def disable(self, render_group, disabled_nests, player):
        """
        Called when the player reaches a nest. Disables the nest for the given player.

        - :param render_group:
            A pygame LayerdUpdates object holding the sprites to be rendered in the game. The nest will be added to this group.
        - :param disabled_nests:
            A list of nests that have already been disabled. This list is independent of the player.disabled_nests attribute.
        - :param player:
            A Player object. This player will have their disabled_nests attribute updated with the nest.
        - :return:
            None
        """
        render_group
        # self.remove(win_group)
        self.image = AssetDictionary.asset_dict["win-frog"]
        self.add(render_group)
        self.add(disabled_nests)
        player.disabled_nests.add(self)
