import pygame.sprite


class DisabledNests(pygame.sprite.Group):

    @staticmethod
    def check_for_win(player):
        """Returns true if the player has reached all 5 nests."""
        if len(player.disabled_nests.sprites()) >= 5:
            return True
        else:
            return False
