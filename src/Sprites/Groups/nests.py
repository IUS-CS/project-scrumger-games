import pygame.sprite


class DisabledNests(pygame.sprite.Group):

    def check_for_win(self):
        if len(self.sprites()) >= 5:
            return True
        else:
            return False
