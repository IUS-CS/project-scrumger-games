import pygame
from Sprites.player import Player
from Util.asset_dictionary import AssetDictionary


def move_player(player: Player, key_depressed, movement_distance_x, movement_distance_y, asset_dict):
    """Handles player movement"""
    x_change = 0
    y_change = 0
    up = 119  # 'w' key ascii
    left = 97  # 'a' key ascii
    right = 100  # 'd' key ascii
    down = 115  # 's' key ascii

    up_image = asset_dict.get_asset("frog")
    up_image2 = asset_dict.get_asset("frog_jumping")
    left_image = pygame.transform.rotate(up_image, 90)
    left_image2 = pygame.transform.rotate(up_image2, 90)
    right_image = pygame.transform.rotate(up_image, -90)
    right_image2 = pygame.transform.rotate(up_image2, -90)
    down_image = pygame.transform.rotate(up_image, 180)
    down_image2 = pygame.transform.rotate(up_image2, 180)

    if key_depressed == up:  # if up key is pressed
        if player.rect.y > 20:  # not at top
            y_change -= movement_distance_y  # move up
            player.images = [up_image, up_image2]

    elif key_depressed == left:  # if left key is pressed
        if player.rect.x > 20:  # not at leftmost border
            x_change -= movement_distance_x
            player.images = [left_image, left_image2]

    elif key_depressed == right:  # if right key is pressed
        if player.rect.x < 750:  # not at rightmost border
            x_change += movement_distance_x
            player.images = [right_image, right_image2]

    elif key_depressed == down:  # if down key is pressed
        if player.rect.y < 800:  # not at bottom
            y_change += movement_distance_y
            player.images = [down_image, down_image2]

    player.rect.x += x_change
    player.rect.y += y_change
