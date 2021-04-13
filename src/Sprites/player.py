import pygame.sprite
import pygame.surface
from Util.window import Window
from Util.utilities import quit_game, pointcollidelist
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
        self.last_advancement = 0
        self.on_sinking_turtle = False
        self.disabled_nests = pygame.sprite.Group()

    def nest(self, timer, nest):
        """Called when the player reaches a nest to return him home and handle the score increase."""
        if self.disabled_nests.has(nest):
            self.kill()
        else:
            self.return_home()
            self.farthest_distance = 900
            self.score += (50 + 2*timer)
            #pygame.time.set_timer(pygame.USEREVENT, 0)  # Reset clock tick so we aren't still using the old clock
            #pygame.time.set_timer(pygame.USEREVENT, 1000)
            timer = 30

    def win_game(self):
        """Called when the player reaches all nests and has won the game."""
        self.score += 1000
        for group in self.groups():
            self.remove(group)
        # quit_game(self)

    def kill(self):
        """Called when the player dies. Returns him home, subtracts a life, and subtracts 10 points from his score.
        Does not subtract points if the player has more than 10."""
        self.return_home()
        self.lives_left -= 1

        if self.lives_left < 0:
            print("player final score: " + str(self.score))
            # quit_game(self)

    def return_home(self):
        """Return the player to the starting position, with the starting sprite orientation."""
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = self.images[self.index]
        self.direction = "up"
        up_image = AssetDictionary.get_asset("frog")
        up_image2 = AssetDictionary.get_asset("frog_jumping")
        self.images = [up_image, up_image2]

    def set_score(self, frame_count):
        """Called on every frame. Handles logic determining when the player should receive more points for moving."""
        self.score += 0.01  # Reward the AI a little bit for staying alive another frame
        if self.farthest_distance > self.rect.y > 110:
            self.farthest_distance = self.rect.y
            self.score += 10
            if self.score > 60 and self.rect.y >= 109:
                self.score += 10
            self.last_advancement = frame_count

    def move(self, key_pressed, frame_count):
        """Called when the AI decides to move, takes a string containg w, a, s, or d, and moves the player in the
        corresponding direction. If any other input is passed, the player won't move at all."""
        if key_pressed == "w" and self.rect.y > 60:
            self.rect.y -= self.y_vel
        elif key_pressed == "s" and self.rect.y < 800:
            self.rect.y += self.y_vel
        elif key_pressed == "a" and self.rect.x > 20:
            self.rect.x -= self.x_vel
        elif key_pressed == "d" and self.rect.x < 750:
            self.rect.x += self.x_vel
        else:
            return

    def find_distance_to_sprite(self, direction, sprites, player_lines):
        """Find the distance to the nearest sprite in a given direction"""
        # Player's current position will be the start point of a line that is used to check the nearest sprite
        player_x = self.rect.center[0]
        player_y = self.rect.center[1]
        player_pos = (player_x, player_y)

        if direction == "ahead":
            distance_to_nearest = player_y

            # Set the endpoint of the line to the top of the screen, in the same x position as the player
            endpoint = (player_x, 0)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites.sprites():
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and player_y - sprite.rect.y <= distance_to_nearest:
                    distance_to_nearest = player_y - sprite.rect.y

            return distance_to_nearest

        if direction == "down":
            distance_to_nearest = Window.HEIGHT - player_y

            # Set the endpoint of the line to the bottom of the screen, in the same x position as the player
            endpoint = (player_x, Window.HEIGHT)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites.sprites():
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and 0 - player_y + sprite.rect.y <= distance_to_nearest:
                    distance_to_nearest = 0 - player_y - sprite.rect.y

            return distance_to_nearest

        if direction == "left":
            distance_to_nearest = player_x

            # Set the endpoint of the line to the left of the screen, in the same y position as the player
            endpoint = (0, player_y)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites.sprites():
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and player_x - sprite.rect.x <= distance_to_nearest:
                    distance_to_nearest = player_x - sprite.rect.x

            return distance_to_nearest

        if direction == "right":
            distance_to_nearest = player_x

            # Set the endpoint of the line to the right of the screen, in the same y position as the player
            endpoint = (Window.WIDTH, player_y)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites.sprites():
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and 0 - player_x + sprite.rect.x <= distance_to_nearest:
                    distance_to_nearest = 0 - player_x + sprite.rect.x

            return distance_to_nearest

    def find_sprite_in_next_lane(self, direction, sprites, player_lines):
        """Find the distance to the nearest sprite in the lane ahead or the lane behind the player
        Returns a tuple containing the distance in the corresponding lane to the closest sprite on the left, and the
        closest sprite on the right, respectively."""

        startpoint_x = self.rect.center[0]

        if direction == "ahead":
            # If the player is at the top of the screen, return the max distance
            if self.rect.y == 109:
                return Window.WIDTH, Window.WIDTH

            # If we want to use the lane ahead,
            # set the start point of the line to be one lane position ahead of the player
            startpoint_y = self.rect.center[1] - 64
            startpoint_pos = (startpoint_x, startpoint_y)

            # Initial distance is the distance to the left and right edges of the screen
            distance_to_left = startpoint_x
            distance_to_right = Window.WIDTH - startpoint_y

            # Set the endpoint of the left line and the right line to the edges of the screen
            left_endpoint = (0, startpoint_y)
            right_endpoint = (Window.WIDTH, startpoint_y)

            # Iterate over the sprites we're concerned about to see if the lines intersect
            for sprite in sprites.sprites():
                # Check the left side
                clipline = sprite.rect.clipline(startpoint_pos, left_endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and startpoint_x - (sprite.rect.x + sprite.rect.width) <= distance_to_left:
                    distance_to_left = startpoint_x - (sprite.rect.x + sprite.rect.width)

                # Check the right side
                clipline = sprite.rect.clipline(startpoint_pos, right_endpoint)

                if clipline and sprite.rect.x - startpoint_x <= distance_to_right:
                    distance_to_right = sprite.rect.x - startpoint_x

            # render lines for debugging
            # player_lines.append((startpoint_pos, (startpoint_x - distance_to_left, startpoint_y)))
            # player_lines.append((startpoint_pos, (startpoint_x + distance_to_right, startpoint_y)))
            return distance_to_left, distance_to_right

        if direction == "down":
            # If the player is at the bottom of the screen, return the max distance
            if self.rect.center[1] + 64 >= Window.HEIGHT:
                return Window.WIDTH, Window.WIDTH

            # If we want to use the lane behind,
            # set the start point of the line to be one lane position behind the player
            startpoint_y = self.rect.center[1] + 64
            startpoint_pos = (startpoint_x, startpoint_y)

            # Initial distance is the distance to the left and right edges of the screen
            distance_to_left = startpoint_x
            distance_to_right = Window.WIDTH - startpoint_y

            # Set the endpoint of the left line and the right line to the edges of the screen
            left_endpoint = (0, startpoint_y)
            right_endpoint = (Window.WIDTH, startpoint_y)

            # Iterate over the sprites we're concerned about to see if the lines intersect
            for sprite in sprites.sprites():
                # Check the left side
                clipline = sprite.rect.clipline(startpoint_pos, left_endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and startpoint_x - (sprite.rect.x + sprite.rect.width) <= distance_to_left:
                    distance_to_left = startpoint_x - (sprite.rect.x + sprite.rect.width)

                # Check the right side
                clipline = sprite.rect.clipline(startpoint_pos, right_endpoint)

                if clipline and sprite.rect.x - startpoint_x <= distance_to_right:
                    distance_to_right = sprite.rect.x - startpoint_x

            return distance_to_left, distance_to_right
