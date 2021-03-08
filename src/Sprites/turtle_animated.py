import pygame.sprite
import pygame.surface
from Sprites.turtle import Turtle


class TurtleSinker(Turtle):
    """Pygame sprite class representing an animated turtle"""

    def __init__(self, frames, frame_spawned_on, x, y):
        Turtle.__init__(self, frames[0], x, y)
        self.frames = frames
        self.last_animation = frame_spawned_on
        self.animation_started = False
        self.image = frames[0]
        self.frame_index = 0
        self.submerged = False
        self.emerging = True

    def start_animation(self, framecount):
        self.animation_started = True
        self.next_frame(framecount)

    def next_frame(self, framecount):

        if not self.submerged and not self.emerging:
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.submerge()
                self.submerged = True
            else:
                self.image = self.frames[self.frame_index]
            self.last_animation = framecount

        elif self.submerged and framecount - self.last_animation > 30:
            self.submerged = False
            self.emerging = True
            self.last_frame()

        elif self.emerging:
            self.last_frame()
            self.last_animation = framecount

    def last_frame(self):
        self.frame_index -= 1
        if self.frame_index < 1:
            self.finish_animation()
        self.image = self.frames[self.frame_index]

    def submerge(self):
        self.submerged = True

    def finish_animation(self):
        self.frame_index = 0
        self.animation_started = False
        self.emerging = False
        self.submerged = False
