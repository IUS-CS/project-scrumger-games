import pygame.sprite
from Sprites.log import Log
from Sprites.turtle import Turtle
from Sprites.turtle_animated import TurtleSinker


class RiverSprites(pygame.sprite.Group):
    """
    Extends the pygame Group class. A custom group class to hold all the turtles, logs, and the WaterSprite.
    """

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def check_if_sunk(self, player, river):
        """
        Called on every frame. Determines if the player is in the river and, if he is, whether he should be killed
        for falling in while riding a turtle that sank. Also sets the player.on_sinking_turtle value for the AI,
        so that it knows when it is on a turtle that could sink.

        - :param player:
            A Player object. This player is checked to see if it has sunk, and is killed if it has. It will also have its
            on_sinking_turtle attribute adjusted if it is on a TurtleSinker sprite on the current frame.
        - :param river:
            A WaterSprite object representing the river. The player is checked that it is colliding with this class
            before any other logic is handled, because if the player isn't in the river then there is no need to do any
            other logic.
        - :return:
            None
        """
        collide_list = pygame.sprite.spritecollide(player, self, False)
        player_center = player.rect.center
        kill_flag = True
        player.on_sinking_turtle = False

        if collide_list and collide_list.count(river):
            collide_list.remove(river)

            for sprite in collide_list:

                if type(sprite) == TurtleSinker:
                    player.on_sinking_turtle = True

                else:
                    player.on_sinking_turtle = False

                if sprite.rect.collidepoint(player_center):
                    if type(sprite) == Log or type(sprite) == Turtle:
                        kill_flag = False

                    elif type(sprite) == TurtleSinker and not sprite.submerged:
                        kill_flag = False

        else:
            kill_flag = False

        if kill_flag:
            player.kill()
