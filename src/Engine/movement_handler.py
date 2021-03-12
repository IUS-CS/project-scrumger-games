import pygame
from Sprites.player import Player
from Util.asset_dictionary import AssetDictionary


def move_player(player: Player, key_depressed, movement_distance_x, movement_distance_y):
    """Handles player movement"""
    x_change = 0
    y_change = 0
    up = 119  # 'w' key ascii
    left = 97  # 'a' key ascii
    right = 100  # 'd' key ascii
    down = 115  # 's' key ascii

    if key_depressed == up:  # if up key is pressed
        if player.rect.y > 60:  # not at top
            y_change -= movement_distance_y  # move up
            up_image = AssetDictionary.get_asset("frog")
            up_image2 = AssetDictionary.get_asset("frog_jumping")
            player.images = [up_image, up_image2]
        new_y = player.rect.y
        if new_y < player.farthest_distance:
            player.farthest_distance = new_y
            player.score += 10

    elif key_depressed == left:  # if left key is pressed
        if player.rect.x > 20:  # not at leftmost border
            x_change -= movement_distance_x
            left_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), 90)
            left_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), 90)
            player.images = [left_image, left_image2]

    elif key_depressed == right:  # if right key is pressed
        if player.rect.x < 750:  # not at rightmost border
            x_change += movement_distance_x
            right_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), -90)
            right_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), -90)
            player.images = [right_image, right_image2]

    elif key_depressed == down:  # if down key is pressed
        if player.rect.y < 800:  # not at bottom
            y_change += movement_distance_y
            down_image = pygame.transform.rotate(AssetDictionary.get_asset("frog"), 180)
            down_image2 = pygame.transform.rotate(AssetDictionary.get_asset("frog_jumping"), 180)
            player.images = [down_image, down_image2]

    player.rect.x += x_change
    player.rect.y += y_change
