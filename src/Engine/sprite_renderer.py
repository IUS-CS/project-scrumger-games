import pygame.display
from Util.window import Window


# Main game drawing function
def draw_sprites(render_group, win, background, text_timer_box, player_lines):
    """Draws the frame to be rendered"""
    win.fill((255, 255, 255))
    win.blit(background, (0, 0))

    for line in player_lines:
        pygame.draw.line(win, pygame.color.Color(255, 10, 10), line[0], line[1], 2)
        player_lines.remove(line)

    # Write over previous number
    win.blit(text_timer_box, (10, 825))

    render_group.draw(win)
    pygame.display.update()
