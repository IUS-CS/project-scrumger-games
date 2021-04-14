import pygame.sprite
import pygame.surface


class Turtle(pygame.sprite.Sprite):
    """Pygame sprite class representing a turtle."""

    def __init__(self, frames, frame_spawned_on, x, y, animation_speed=8):
        """
        - :param frames:
            A list of images which will be cycled through to animate the turtles.
        - :param frame_spawned_on:
            An int representing the frame that the turtle spawned on. Used to handle animation logic.
        - :param x:
            The starting x position of the turtle.
        - :param y:
            The startying y position of the turtle.
        - :param animation_speed:
            Optional. An int representing the speed at which the turtle will be animated. The animator will wait this many frames
            before advancing the turtle's animation. Defaults to 8.
        """
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.image = frames[0]
        self.frame_index = 0
        self.rect = self.image.get_rect()
        self.animation_speed = animation_speed
        self.last_animation = frame_spawned_on

        self.rect.x = x
        self.rect.y = y

    def next_frame(self, framecount):
        """
        Determines if the turtle animation should advance a frame, and advances it if so.

        - :param framecount:
            An int containing the current frame being rendered. Used to determine if the animation should advance.
        - :return:
            None
        """
        if framecount - self.last_animation >= self.animation_speed:

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[self.frame_index]
            self.last_animation = framecount
