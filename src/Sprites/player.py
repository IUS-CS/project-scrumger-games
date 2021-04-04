import pygame.sprite
import pygame.surface
from Util.window import Window
from Util.utilities import quit_game
from Util.asset_dictionary import AssetDictionary


class Player(pygame.sprite.Sprite):
    """Pygame sprite class representing the player"""

    def __init__(self, render_group, images=AssetDictionary.get_asset("player")):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = images[self.index]
        self.direction = "up"
        self.score = 0
        self.farthest_distance = 900
        self.lives_left = 6
        self.add(render_group)
        render_group.change_layer(self, 1)
        self.can_move = True
        self.x_vel = AssetDictionary.get_asset("frog").get_width() + 4
        self.y_vel = AssetDictionary.get_asset("frog").get_height() + 12
        self.timer = 30

    def nest(self):
        self.return_home()
        self.farthest_distance = 900
        self.score += (50 + 2*Window.TIMER)
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Reset clock tick so we aren't still using the old clock
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        Window.TIMER = 30
        Window.TIMER_TEXT = str(Window.TIMER).rjust(5)

    def win_game(self):
        self.score += 1000
        quit_game(self)

    def kill(self):
        self.return_home()
        self.lives_left -= 1
        self.timer = 30
        Window.TIMER_TEXT = str(Window.TIMER).rjust(5)

        if self.lives_left < 0:
            print("player final score: " + str(self.score))
            quit_game(self)

    def return_home(self):
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = self.images[self.index]
        self.direction = "up"
        up_image = AssetDictionary.get_asset("frog")
        up_image2 = AssetDictionary.get_asset("frog_jumping")
        self.images = [up_image, up_image2]

    def set_score(self):
        if self.farthest_distance > self.rect.y > 110:
            self.farthest_distance = self.rect.y
            self.score += 10

    def move(self, key_pressed):
        if key_pressed == "w" and self.rect.y > 60:
            self.rect.y -= self.y_vel
            self.set_score()
        elif key_pressed == "s" and self.rect.y < 800:
            self.rect.y += self.y_vel
        elif key_pressed == "a" and self.rect.x > 20:
            self.rect.x -= self.x_vel
        elif key_pressed == "d" and self.rect.x < 750:
            self.rect.x += self.x_vel
        else:
            return

    def find_distance_to_sprite(self, direction):
        """Find the distance to the nearest sprite in a given direction"""
        if direction == "ahead":
            line = (self.rect.x, self.rect.y, self.rect.center[0], 0)

            for sprite in Window.SPRITE_LIST:
                if sprite.rect.clipline(line) != ():
                    return self.rect.y - sprite.rect.y

            return self.rect.y - Window.HEIGHT

        if direction == "down":
            line = (self.rect.x, self.rect.y, self.rect.center[0], Window.HEIGHT)

            for sprite in Window.SPRITE_LIST:
                if sprite.rect.clipline(line) != ():
                    return self.rect.y - sprite.rect.y

            return self.rect.y - Window.HEIGHT

        elif direction == "left":
            line = (self.rect.x, self.rect.y, 0, self.rect.center[1])

            for sprite in Window.SPRITE_LIST:
                if sprite.rect.clipline(line) != ():
                    return self.rect.x - sprite.rect.x

            return self.rect.x - Window.HEIGHT

        elif direction == "right":
            line = (self.rect.x, self.rect.y, Window.WIDTH, self.rect.center[1])

            for sprite in Window.SPRITE_LIST:
                if sprite.rect.clipline(line) != ():
                    return self.rect.x - sprite.rect.x

            return self.rect.x - Window.HEIGHT

