import pygame.display


# Main game drawing function
def draw_sprites(render_group, win, background, text_timer_box):
    """Draws the frame to be rendered"""
    win.fill((255, 255, 255))
    win.blit(background, (0, 0))

    #Write over previous number
    win.blit(text_timer_box, (10, 825))

    render_group.draw(win)
    pygame.display.update()
