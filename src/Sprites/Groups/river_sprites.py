import pygame.sprite
from Sprites.log import Log
from Sprites.turtle import Turtle
from Sprites.turtle_animated import TurtleSinker
from Sprites.water import WaterSprite


class RiverSprites(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def check_if_sunk(self, player, river):
        collide_list = pygame.sprite.spritecollide(player, self, False)
        player_center = player.rect.center
        kill_flag = True

        if collide_list and self.has(river):
            collide_list.remove(river)

            for sprite in collide_list:
                if sprite.rect.collidepoint(player_center):
                    if type(sprite) == Log or type(sprite) == Turtle:
                        kill_flag = False

                    elif type(sprite) == TurtleSinker and not sprite.submerged:
                        kill_flag = False

        else:
            kill_flag = False

        if kill_flag:
            player.kill()
