import pygame
from Sprites.player import Player
from Sprites.turtle_animated import TurtleSinker


def animate_sprites(*args):
    animate_turtles(args[0], args[1], args[2], args[3])


def animate_lane(lane, framecount, net_group):
    for sprite in lane.sprites():
        if isinstance(sprite, TurtleSinker):
            if not sprite.animation_started and framecount - sprite.last_animation >= 30:
                sprite.start_animation(framecount, net_group)

            else:
                sprite.next_frame(framecount, net_group)

        elif not isinstance(sprite, Player):
            sprite.next_frame(framecount)


def animate_turtles(lane1: pygame.sprite.Group, lane2: pygame.sprite.Group, framecount, net_group):

    animate_lane(lane1, framecount, net_group)
    animate_lane(lane2, framecount, net_group)
