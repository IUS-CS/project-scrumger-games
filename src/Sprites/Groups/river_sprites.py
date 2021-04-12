import pygame.sprite
from Sprites.log import Log
from Sprites.turtle import Turtle
from Sprites.turtle_animated import TurtleSinker


class RiverSprites(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def check_if_sunk(self, player, river):
        collide_list = pygame.sprite.spritecollide(player, self, False)
        player_center = player.rect.center
        kill_flag = True
        player.on_sinking_turtle = False

        if collide_list and collide_list.count(river):
            collide_list.remove(river)

            for sprite in collide_list:

                if type(sprite) == TurtleSinker:
                    player.on_sinking_turtle = True

                if sprite.rect.collidepoint(player_center):
                    if type(sprite) == Log or type(sprite) == Turtle:
                        kill_flag = False

                    elif type(sprite) == TurtleSinker and not sprite.submerged:
                        kill_flag = False

        else:
            kill_flag = False

        if kill_flag:
            player.kill()
