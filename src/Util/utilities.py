import pygame
from Util.window import Window


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


def add_river_sprites_to_group(lanes, river_group):
    """Adds all of the sprites in the water lanes to the river group for kill detection"""
    for group in lanes:
        for sprite in group:
            sprite.add(river_group)


def add_player_to_water_lane(lanes, player):
    for lane in lanes:
        lane.remove(player)

    if player.rect.y == 365:
        player.add(lanes[0])
    elif player.rect.y == 301:
        player.add(lanes[1])
    elif player.rect.y == 237:
        player.add(lanes[2])
    elif player.rect.y == 173:
        player.add(lanes[3])
    elif player.rect.y == 109:
        player.add(lanes[4])


def check_kill_collisions(player, kill_group):
    """Checks the player sprite object against a group object
       and kills the sprite if it collides with any sprite in the group"""
    collide_list = pygame.sprite.spritecollide(player, kill_group, False)
    if collide_list:
        player.kill()


def check_win_collisions(player, win_group, render_group, kill_group, disabled_nests):
    """Checks the player sprite object against a group object for the game's win condition"""
    collide_list = pygame.sprite.spritecollide(player, win_group, True)
    if collide_list:
        player.nest()
        for nest in collide_list:
            nest.disable(win_group, render_group, kill_group, disabled_nests)

        if disabled_nests.check_for_win():
            player.win_game()


def quit_game(player):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    Window.FINAL_SCORE = player.score
    print("Final score: " + str(Window.FINAL_SCORE))
