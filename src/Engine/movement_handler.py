from Sprites.player import Player


def move_player(player: Player, key_depressed, movement_distance_x, movement_distance_y):
    """Handles player movement"""
    x_change = 0
    y_change = 0
    up = 119  # 'w' key ascii
    left = 97  # 'a' key ascii
    right = 100  # 'd' key ascii
    down = 115  # 's' key ascii

    if key_depressed == up:  # if up key is pressed
        if player.rect.y > 20:  # not at top
            y_change -= movement_distance_y  # move up

    elif key_depressed == left:  # if left key is pressed
        if player.rect.x > 20:  # not at leftmost border
            x_change -= movement_distance_x

    elif key_depressed == right:  # if right key is pressed
        if player.rect.x < 750:  # not at rightmost border
            x_change += movement_distance_x

    elif key_depressed == down:  # if down key is pressed
        if player.rect.y < 800:  # not at bottom
            y_change += movement_distance_y

    player.rect.x += x_change
    player.rect.y += y_change
