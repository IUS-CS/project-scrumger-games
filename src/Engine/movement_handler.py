import pygame
from Sprites.player import Player
from Util.asset_dictionary import AssetDictionary


def move_player(player: Player, key_depressed, movement_distance_x, movement_distance_y, sound_effect):
    """
    Handles player movement when the AI is not being trained. This should only be called when the game is being played
    by a human.

    - :param player:
        A Player object.
    - :param key_depressed:
        An int representing the key that was pressed to call the function. 119 for moving up, 97 for left, 100 for right, 115 for down. These correspond to WASD.
    -:param movement_distance_x:
        An int representing the distance a player will move in the horizontal directions
    :param movement_distance_y:
        An int representing the distance a player will move in the vertical directions
    - :param sound_effect:
        A sound effect asset to be played when the player moves
    - :return:
        None
    """
    x_change = 0
    y_change = 0
    up = 119  # 'w' key ascii
    left = 97  # 'a' key ascii
    right = 100  # 'd' key ascii
    down = 115  # 's' key ascii

    if key_depressed == up:  # if up key is pressed
        if player.rect.y > 60:  # not at top
            sound_effect.play()
            y_change -= movement_distance_y  # move up
            up_image = AssetDictionary.get_asset("frog")
            up_image2 = AssetDictionary.get_asset("frog_jumping")
            player.images = [up_image, up_image2]
        new_y = player.rect.y
        if player.farthest_distance > new_y > 110:
            player.farthest_distance = new_y
            player.score += 10

    elif key_depressed == left:  # if left key is pressed
        if player.rect.x > 20:  # not at leftmost border
            sound_effect.play()
            x_change -= movement_distance_x
            left_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), 90)
            left_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), 90)
            player.images = [left_image, left_image2]

    elif key_depressed == right:  # if right key is pressed
        if player.rect.x < 750:  # not at rightmost border
            sound_effect.play()
            x_change += movement_distance_x
            right_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), -90)
            right_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), -90)
            player.images = [right_image, right_image2]

    elif key_depressed == down:  # if down key is pressed
        if player.rect.y < 800:  # not at bottom
            sound_effect.play()
            y_change += movement_distance_y
            down_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), 180)
            down_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), 180)
            player.images = [down_image, down_image2]

    player.rect.x += x_change
    player.rect.y += y_change
