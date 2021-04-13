import pygame.sprite

from Sprites.turtle import Turtle


class TurtleSinker(Turtle):
    """Pygame sprite class representing an animated turtle"""

    def __init__(self, frames, frame_spawned_on, x, y, animation_speed=18):
        Turtle.__init__(self, frames, frame_spawned_on, x, y)
        self.animation_started = False
        self.submerged = False
        self.emerging = False
        self.animation_speed = animation_speed

    def start_animation(self, framecount, net_group):
        """Called when the turtle's sinking animation should start."""
        self.animation_started = True
        self.next_frame(framecount, net_group)

    def next_frame(self, framecount, net_group):
        """Called on every frame, determines if the turtle's sinking animation should be advanced and advances it
        if so. Also handles reversing it for the turtle's emerge animation. Additionally, this function handles the
        removal of a turtle from the net_group used to let the AI 'see' sprites, so the AI knows when a turtle is
        submerged and not safe to jump on."""
        if self.animation_started:

            if not self.submerged and not self.emerging and self.should_animate(framecount):  # start new submerge cycle
                self.frame_index += 1
                if self.frame_index > 2:  # if at the end of submerge animation, set submerged state
                    self.submerged = True
                    self.remove(net_group)
                    self.image = self.frames[self.frame_index]
                    self.last_animation = framecount
                else:                                     # otherwise, advance the animation
                    self.image = self.frames[self.frame_index]
                    self.last_animation = framecount

            # turtle is submerged - begin emerge animation
            elif self.submerged and self.should_animate(framecount):
                self.submerged = False
                self.add(net_group)
                self.emerging = True
                self.last_frame()
                self.last_animation = framecount

            # turtle is emerging - play submerge animation backwards
            elif self.emerging and self.should_animate(framecount):
                self.last_frame()
                self.last_animation = framecount

    def last_frame(self):
        """Called when the turtle is emerging. Advance the animation fram backwards by one."""
        self.frame_index -= 1
        if self.frame_index < 1:
            self.finish_animation()
        self.image = self.frames[self.frame_index]

    def finish_animation(self):
        """Called when the emerge animation is finished. Ensures that all the turtle attributes are reset to the
        starting state."""
        self.frame_index = 0
        self.animation_started = False
        self.emerging = False
        self.submerged = False

    def should_animate(self, framecount):
        """Determines if the turtle should advance to the next frame based on the animation speed attribute."""
        return framecount - self.last_animation >= self.animation_speed
