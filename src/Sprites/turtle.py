import pygame.sprite
import pygame.surface


class Turtle(pygame.sprite.Sprite):
    """Pygame sprite class representing a turtle"""

    def __init__(self, frames, frame_spawned_on, x, y, animation_speed=8):
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
        """Determines if the animation should advance a frame, and advances it if so."""
        if framecount - self.last_animation >= self.animation_speed:

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[self.frame_index]
            self.last_animation = framecount
