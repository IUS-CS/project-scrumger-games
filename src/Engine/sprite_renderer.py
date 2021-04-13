import pygame.display


# Main game drawing function
def draw_sprites(render_group, win, background, player_lines):
    """Draws the frame to be rendered"""
    win.blit(background, (0, 0))

    # for line in player_lines:
    #     pygame.draw.line(win, pygame.color.Color(255, 10, 10), line[0], line[1], 2)
    #     player_lines.remove(line)

    render_group.draw(win)
    pygame.display.update()
