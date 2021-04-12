import pygame
import pygame.locals
from Util.window import Window


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


def add_sprites_to_group(lanes, group):
    """Adds all of the sprites in the water lanes to the river group for kill detection"""
    for lane in lanes:
        for sprite in lane:
            sprite.add(group)


def add_player_to_water_lane(lanes, player):
    """Checks the position of the player and adds them to the appropriate water lane group for log and turtle riding"""
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


def check_win_collisions(player, win_group, render_group, kill_group, disabled_nests, timers):
    """Checks the player sprite object against a group object for the game's win condition"""
    collide_list = pygame.sprite.spritecollide(player, win_group, True)
    if collide_list:
        for nest in collide_list:
            player.nest(timers[0], nest)
            nest.disable(win_group, render_group, kill_group, disabled_nests, player)

        if disabled_nests.check_for_win():
            player.win_game()


def pointcollidelist(point, sprite_list: pygame.sprite.Group):
    """Checks a point against a list of sprites for collisions, and returns the first sprite in the list if a collision
    is found, otherwise returns false."""
    for sprite in sprite_list:
        if sprite.rect.collidepoint(point):
            return sprite

    return False


def parse_if_training_net(argv):
    """Parses the list of command line arguments, returns the argument after -t or -train if it is present,
     returns false otherwise. If not false, this argument should be the number of generations the user wishes to run."""
    arg_list = []
    for arg in enumerate(argv):
        arg_list.append(arg[1])

    try:
        index = arg_list.index("-t")

    except ValueError:
        try:
            index = arg_list.index("-train")

        except ValueError:
            return False

    return arg_list[index + 1]


def determine_keypress(index):
    """Takes the index of the max value of a neural net output layer, and returns the appropriate keypress event"""
    if index == 0:
        return "w"
    elif index == 1:
        return "a"
    elif index == 2:
        return "s"
    elif index == 3:
        return "d"
    else:
        return None


def quit_game(player):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    Window.FINAL_SCORE = player.score
    return Window.FINAL_SCORE
