import pygame.sprite
import pygame.surface
from Util.window import Window
from Util.asset_dictionary import AssetDictionary


class Player(pygame.sprite.Sprite):
    """
    Pygame sprite class representing the player. Constructor should be passed a pygame LayeredUpdates object to
    which the Player object will be added. By default, this class will get the list of image assets used for animating
    the frog's jump, but a different list of two image assets can be passed. The frog will animate between these
    two images when the player (not the AI) moves the frog.
    """

    def __init__(self, render_group, images=AssetDictionary.get_asset("player")):
        """
        - :param render_group:
            The pygame Group object containing all of the sprites to be rendered on the current frame
        - :param images:
            Optional. A list of image assets between which the sprite will animate when a human player moves the frog.
            Defaults to the "player" image asset found in the asset dictionary in utilities.
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = images[self.index]
        self.direction = "up"
        self.score = 0
        self.farthest_distance = 813
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
        """
        Called when the player reaches a nest to return him home and handle the score increase.

        - :param timer:
            An int representing the current timer value.
        - :param nest:
            A Nest object, should be the nest that the player reached to trigger this method to be called
        - :return:
            None
        """
        if self.disabled_nests.has(nest):
            self.kill()
        else:
            self.return_home()
            self.farthest_distance = 813
            self.score += (50 + 2*timer)
            # pygame.time.set_timer(pygame.USEREVENT, 0)  # Reset clock tick so we aren't still using the old clock
            # pygame.time.set_timer(pygame.USEREVENT, 1000)
            # timer = 30
        if not self.disabled_nests.has(nest):
            self.disabled_nests.add(nest)

    def win_game(self):
        """
        Called when the player reaches all nests and has won the game. Adds 2000 to the player's score and removes them
        from all groups they are in so they will no longer be rendered.

        - :return:
            None
        """
        self.score += 2000
        for group in self.groups():
            self.remove(group)
        # quit_game(self)

    def kill(self):
        """
        Called when the player dies. Returns him home, and subtracts a life from his life_count.

        - :return:
            None
        """
        self.return_home()
        self.lives_left -= 1

        # if self.lives_left < 0:
        #     print("player final score: " + str(self.score))
        #     quit_game(self)

    def return_home(self):
        """
        Return the player to the starting position, with the starting sprite orientation.

        - :return:
            None
        """
        self.rect.x = Window.WIN.get_width() / 2
        self.rect.y = Window.WIN.get_height() - self.rect.height - 11
        self.index = 0
        self.image = self.images[self.index]
        self.direction = "up"
        up_image = AssetDictionary.get_asset("frog")
        up_image2 = AssetDictionary.get_asset("frog_jumping")
        self.images = [up_image, up_image2]

    def set_score(self):
        """
        Called on every frame. Handles the logic determining when the player should receive more points for moving.

        - :return:
            None
        """

        # If the current position is a new farthest distance, increase the score
        if self.farthest_distance > self.rect.y > 110:
            self.farthest_distance = self.rect.y
            self.score += 10
            if self.score > 60 and self.rect.y >= 109:
                self.score += 10

    def move(self, key_pressed, frame_count):
        """
        Called when the AI computes an output layer. Takes a string containing w, a, s, or d, and moves the player
        in the corresponding direction. If any other input is passed, the player won't move at all.

        - :param key_pressed:
            A string that should contain w, a, s, or d corresponding to the desired direction to move. Anything else
            causes the player to do nothing.
        - :param frame_count:
            An int representing the current frame count of the game.
        - :return:
            None
        """
        if key_pressed == "w" and self.rect.y > 60:
            self.rect.y -= self.y_vel
            self.last_advancement = frame_count
        elif key_pressed == "s" and self.rect.y < 800:
            self.rect.y += self.y_vel
        elif key_pressed == "a" and self.rect.x > 20:
            self.rect.x -= self.x_vel
        elif key_pressed == "d" and self.rect.x < 750:
            self.rect.x += self.x_vel
        else:
            return

    def find_distance_to_sprite(self, direction, sprites, player_lines=[]):
        """
        Find the distance to the nearest sprite in a given direction. Calculates from the center point of the
        player to the sprite.rect.x or sprite.rect.y coordinate of the nearest sprite. Whether x or y is used depends
        on whether the direction being computed is vertical or horizontal - y for up or down and x for left or right.
        Parameter direction should be a string containing 'ahead', 'down', 'left', or 'right' indicating the
        direction we wish to scan. Sprites should be a list of all the sprites that we want to 'see', which will be
        iterated over to scan for a sprite in the given direction. The player_lines parameter can be used to draw
        lines to the sprite for debugging, but defaults to empty.

        - :param direction:
            A string containing the direction to be searched. Should be "ahead", "down", "left", or "right". Anything else,
            and the function will return nothing.
        - :param sprites:
            A pygame Group object containing the sprites to be searched. Should be the Group object used for the AI to "see"
            other sprites.
        - :param player_lines:
            Optional debugging parameter. A list of tuples representing the endpoints of a line. This can be appended to
            in order to render the collision lines for debugging purposes.
        - :return:
            None
        """
        # Player's current position will be the start point of a line that is used to check the nearest sprite
        player_x = self.rect.center[0]
        player_y = self.rect.center[1]
        player_pos = (player_x, player_y)

        if direction == "ahead":
            distance_to_nearest = player_y

            # Set the endpoint of the line to the top of the screen, in the same x position as the player
            endpoint = (player_x, 0)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites:
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
            for sprite in sprites:
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and sprite.rect.y - player_y <= distance_to_nearest:
                    distance_to_nearest = sprite.rect.y - player_y

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
                if clipline and player_x - (sprite.rect.x + sprite.rect.width) <= distance_to_nearest:
                    distance_to_nearest = player_x - (sprite.rect.x + sprite.rect.width)

            return distance_to_nearest

        if direction == "right":
            distance_to_nearest = Window.WIDTH - player_x

            # Set the endpoint of the line to the right of the screen, in the same y position as the player
            endpoint = (Window.WIDTH, player_y)

            # Iterate over the sprites we're concerned about to see if the line intersects
            for sprite in sprites.sprites():
                clipline = sprite.rect.clipline(player_pos, endpoint)

                # If the line intersects with the sprite in question, and the distance to it is shorter than current,
                # update current distance
                if clipline and sprite.rect.x - player_x <= distance_to_nearest:
                    distance_to_nearest = sprite.rect.x - player_x

            return distance_to_nearest

    def find_sprite_in_next_lane(self, direction, sprites, player_lines=[]):
        """
        Find the distance to the nearest sprite in the lane ahead or the lane behind the player. Returns a tuple
        containing the distance in the corresponding lane to the edge of the closest sprite on the left,
        and the closest sprite on the right, respectively. These distances will be measured from the x position of the
        center of the player rect.

        - :param direction:
            A string indicating whether the lane ahead is being searched or the lane behind. Should be "ahead" or "down".
            Anything else, and the method won't return anything.
        - :param sprites:
            A pygame Group object containing the sprites to be searched. Should be the Group object used for the AI to "see"
            other sprites.
        - :param player_lines:
            Optional debugging parameter. A list of tuples representing the endpoints of a line. This can be appended to
            in order to render the collision lines for debugging purposes.
        - :return:
            None
        """

        startpoint_x = self.rect.center[0]

        if direction == "ahead":
            # If we want to use the lane ahead,
            # set the start point of the line to be one lane position ahead of the player
            startpoint_y = self.rect.center[1] - 64
            startpoint_pos = (startpoint_x, startpoint_y)

            # Initial distance is the distance to the left and right edges of the screen
            distance_to_left = startpoint_x
            distance_to_right = Window.WIDTH - startpoint_x

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
            # If we want to use the lane behind,
            # set the start point of the line to be one lane position behind the player
            startpoint_y = self.rect.center[1] + 64
            startpoint_pos = (startpoint_x, startpoint_y)

            # Initial distance is the distance to the left and right edges of the screen
            distance_to_left = startpoint_x
            distance_to_right = Window.WIDTH - startpoint_x

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
