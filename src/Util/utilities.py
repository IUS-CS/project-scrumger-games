import pygame


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


def check_kill_collisions(player: pygame.sprite.Sprite, kill_group: pygame.sprite.Group):
    """Checks the player sprite object against a group object
       and kills the sprite if it collides with any sprite in the group"""
    collide_list = pygame.sprite.spritecollide(player, kill_group, 0)
    if collide_list:
        player.kill()


def check_win_collisions(player: pygame.sprite.Sprite, win_group: pygame.sprite.Group):
    """Checks the player sprite object against a group object for the game's win condition"""
    collide_list = pygame.sprite.spritecollide(player, win_group, 0)
    if collide_list:
        player.win()

