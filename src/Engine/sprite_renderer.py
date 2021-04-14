import pygame.display


# Main game drawing function
def draw_sprites(render_group, win, background):
    """
    Draws the frame to be rendered.

    - :param render_group:
        A pygame LayeredUpdates sprite group which contains all of the sprites to be rendered on the given frame
    - :param win:
        A pygame Surface object on which the sprites will be rendered
    - :param background:
        An image containing the game background. Must already be scaled correctly.
    - :return:
        None
    """
    win.blit(background, (0, 0))

    # for line in player_lines:
    #     pygame.draw.line(win, pygame.color.Color(255, 10, 10), line[0], line[1], 2)
    #     player_lines.remove(line)

    render_group.draw(win)
    pygame.display.update()
