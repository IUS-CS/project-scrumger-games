import pygame
from Sprites.turtle_animated import TurtleSinker


def animate_sprites(*args):
    animate_turtles(args[0], args[1], args[2])

def animate_turtles(lane1: pygame.sprite.Group, lane2: pygame.sprite.Group, framecount):

    animation_speed = 20

    for sprite in lane1.sprites():
        if isinstance(sprite, TurtleSinker):
            if not sprite.animation_started and framecount - sprite.last_animation >= 90:
                sprite.start_animation(framecount)

            else:
                if framecount - sprite.last_animation >= animation_speed:
                    sprite.next_frame(framecount)

    for sprite in lane2.sprites():
        if isinstance(sprite, TurtleSinker):
            if not sprite.animation_started and framecount - sprite.last_animation >= 90:
                sprite.start_animation(framecount)

            else:
                if framecount - sprite.last_animation >= animation_speed:
                    sprite.next_frame(framecount)
