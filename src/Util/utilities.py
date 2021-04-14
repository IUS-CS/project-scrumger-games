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
    """
    Checks the player sprite object against a group object
    and kills the sprite if it collides with any sprite in the group

    - :param player:
        A Player object to be checked against the kill group to see if it has collided with a sprite that should kill it.
    - :param kill_group:
        A pygame Group object containing all of the deadly sprites. If the player has collided with one of these sprites,
        it will be killed.
    - :return:
        None
    """
    collide_list = pygame.sprite.spritecollide(player, kill_group, False)
    if collide_list:
        player.kill()


def check_win_collisions(player, win_group, render_group, kill_group, disabled_nests, timer):
    """
    Checks the player sprite object against a group object for the game's win condition. If the player collides with a
    nest sprite, it will be disabled and player.nest() will be called. If the player has reached all of the nests,
    player.win_game() will be called.

    - :param player:
        A Player object to be checked against the win group to see if it has entered one of the nests.
    - :param win_group:
        A pygame Group object containing all of the Nest sprites that constitute the game's win condition.
    - :param render_group:
        A pygame Group object containing all of the sprites to be rendered on the current frame. If the player has reached
        a nest, it will be added to the render group so a visual indication can be seen that the nest has been reached.
    - :param kill_group:
        A pygame Group object containing all of the deadly sprites. When a nest is reached, it is disabled and added to
        this group so that subsequent collisions with that nest will result in a death.
    - :param disabled_nests:
        A DisabledNests object containing all of the nests that have been disabled so far in the game.
    - :param timer:
        An int representing the number of seconds left on the game timer.
    - :return:
        None
    """
    collide_list = pygame.sprite.spritecollide(player, win_group, True)
    if collide_list:
        for nest in collide_list:
            player.nest(timer, nest)
            nest.disable(render_group, disabled_nests, player)

        if disabled_nests.check_for_win(player):
            player.win_game()


def pointcollidelist(point, sprite_list: pygame.sprite.Group):
    """
    Checks a point against a list of sprites for collisions, and returns the first sprite in the list if a collision
    is found, otherwise returns false.

    - :param point:
        A tuple containing the coordinates of a point in (x, y) format.
    - :param sprite_list:
        A pygame Group object containing the sprites to be checked for collision with the point.
    - :return:
        A pygame Sprite class, or an extension of one, that is the first sprite in the list that the point is found to
        collide with.
    """
    for sprite in sprite_list:
        if sprite.rect.collidepoint(point):
            return sprite

    return False


def parse_if_training_net(argv):
    """
    Parses the list of command line arguments, returns the argument after -t or -train if it is present,
    returns false otherwise. If not false, the argument after -t argument should be the number of generations the user
    wishes to train for.

    - :param argv:
        The list of command line argyments retrieved from sys.argv.
    :return:
        The argument after -t or -train if either of those flags are present. If they are not, returns false.
    """
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
    """
    Determines the appropriate key to press for a given index. Utility function to convert the index of the maximum
    output value from the neural net into a string containing w, a, s, or d. Returns None if the maximum value from the
    output layer is found at index 4.

    - :param index:
        An int containing the index of the maximum value from the output layer of the neural network.
    - :return:
        A string containing "w", "a", "s", or "d", or None.
    """
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
    """
    Pushes pygame.QUIT event to the event queue to end the game.

    - :param player:
        A Player object. Its score is set as the Window.FINAL_SCORE value.
    - :return:
        None
    """
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    Window.FINAL_SCORE = player.score
    return Window.FINAL_SCORE
