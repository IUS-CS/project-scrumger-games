import pygame.sprite


class DisabledNests(pygame.sprite.Group):
    """
    Contains a static method used to check if all the nests have been reached, and activate the win condition.
    """

    @staticmethod
    def check_for_win(player):
        """
        Returns true if the player has reached all 5 nests.

        - :param player:
            A Player object. This player is checked for the win condition.
        - :return:
            None
        """
        if len(player.disabled_nests.sprites()) >= 5:
            return True
        else:
            return False
