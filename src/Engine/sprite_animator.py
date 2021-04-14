import pygame
from Sprites.player import Player
from Sprites.turtle_animated import TurtleSinker


def animate_sprites(*args):
    """
    Helper function used for animating turtles.

    - :param args:
        A list containing two lanes of turtles to be animated, the current frame count, and the net_group used to let the neural network 'see' sprites, respectively
    - :return:
        None
    """
    animate_turtles(args[0], args[1], args[2], args[3])


def animate_lane(lane, framecount, net_group):
    """
    Contains the logic that starts and advances the animation of one lane of turtles at the appropriate times.

    - :param lane:
        A pygame sprite Group object containing all of the turtles in one "lane". The function handles determining which turtles to animate and when.
    - :param framecount:
        An int containing the count of the current frame being rendered
    - :param net_group:
        A pygame sprite Group object containing all of the sprites which we want the AI to "see"
    - :return:
        None
    """
    for sprite in lane.sprites():
        if isinstance(sprite, TurtleSinker):
            if not sprite.animation_started and framecount - sprite.last_animation >= 30:
                sprite.start_animation(framecount, net_group)

            else:
                sprite.next_frame(framecount, net_group)

        elif not isinstance(sprite, Player):
            sprite.next_frame(framecount)


def animate_turtles(lane1: pygame.sprite.Group, lane2: pygame.sprite.Group, framecount,
                    net_group=pygame.sprite.Group()):
    """
    Helper function. Animates each individual lane of turtles.

    - :param lane1:
        A pygame sprite Group object containing all of the turtles in one "lane"
    - :param lane2:
        A pygame sprite Group object containing all of the turtles in one "lane"
    - :param framecount:
        An int containing count of the current frame being rendered
    - :param net_group:
        A pygame sprite Group object containing all of the sprites which we want the AI to "see"
    - :return:
        None
    """
    animate_lane(lane1, framecount, net_group)
    animate_lane(lane2, framecount, net_group)
