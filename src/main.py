# File: main.py
# Authors: John Cooke, Zion Emond
# Since: 2/12/2021
# This file contains the main game loop and will initialize all the game systems
"""
This module will contain the main high level functions of the game, as well as the main game loop
"""
import logging
import os
import pygame

WIDTH, HEIGHT = 820, 876
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Froggerithm")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
current_dir = os.path.dirname(os.path.abspath(__file__))


class Player(pygame.sprite.Sprite):
    """Pygame sprite class representing the player"""

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - self.rect.height - 9


class Car(pygame.sprite.Sprite):
    """Pygame sprite class representing a car"""

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH - self.rect.width
        self.rect.y = 700


class FrogNest(pygame.sprite.Sprite):
    """Pygame sprite class for frog nests used for checking the win condition"""

    # Constructor should be passed an int to indicate which nest position the sprite should go in
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([74, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = 40
        self.set_pos(pos)

    def set_pos(self, pos):
        if pos == 1:
            self.rect.x = 67

        elif pos == 2:
            self.rect.x = 227

        elif pos == 3:
            self.rect.x = 387

        elif pos == 4:
            self.rect.x = 547

        else:
            self.rect.x = 707


class DeathSprites(pygame.sprite.Group):
    """Pygame group class to be used for sprites that should kill the player on collision"""

    def __init__(self):
        pygame.sprite.Group.__init__(self)


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


# Stub method to be called when the player wins the game
def win_game():
    print("YOU WIN!")


def check_kill_collisions(player, kill_group):
    """Checks the player sprite object against a group object
       and kills the sprite if it collides with any sprite in the group"""
    collide_list = pygame.sprite.spritecollide(player, kill_group, 0)
    if collide_list:
        player.kill()


def check_win_collisions(player, win_group):
    """Checks the player sprite object against a group object for the game's win condition"""
    collide_list = pygame.sprite.spritecollide(player, win_group, 0)
    if collide_list:
        win_game()


# Load background image
background_image = pygame.image.load(os.path.join(current_dir, "Assets", "background.png"))
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load sprites into a dictionary for easy reference
asset_dict = {
    "frog": pygame.image.load(os.path.join(current_dir, "Assets", "frog.png")),
    "frog_jumping": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
    "car1": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
    "car2": pygame.image.load(os.path.join(current_dir, "Assets", "car-2.png")),
    "car3": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
    "car4": pygame.image.load(os.path.join(current_dir, "Assets", "car-1.png")),
    "log-long": pygame.image.load(os.path.join(current_dir, "Assets", "log-long.png")),
    "log-short": pygame.image.load(os.path.join(current_dir, "Assets", "log-short.png")),
    "logo": pygame.image.load(os.path.join(current_dir, "Assets", "logo.png")),
    "semi-truck": pygame.image.load(os.path.join(current_dir, "Assets", "semi-truck.png")),
    "turtle-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-1.png")),
    "turtle-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-2.png")),
    "turtle-3": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-3.png")),
    "turtle-sink-1": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-1.png")),
    "turtle-sink-2": pygame.image.load(os.path.join(current_dir, "Assets", "turtle-sink-2.png")),
}

# Scale all the images in the asset dictionary
for key in asset_dict:
    asset_dict[key] = scale_image(asset_dict[key])

MOVEMENT_DISTANCE_X = asset_dict["frog"].get_width() + 4
MOVEMENT_DISTANCE_Y = asset_dict["frog"].get_height() + 12


# Main game drawing function
def draw_window(render_group):
    """Draws the frame to be rendered"""
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))
    render_group.draw(WIN)
    pygame.display.update()


def log_game():
    """Initializes console for logging messages"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Welcome to The Froggerithm!")


def move_player(player: Player, key_depressed):
    """Handles player movement"""
    x_change = 0
    y_change = 0
    up = 119  # 'w' key ascii
    left = 97  # 'a' key ascii
    right = 100  # 'd' key ascii
    down = 115  # 's' key ascii

    if key_depressed == up:  # if up key is pressed
        if player.rect.y > 20:  # not at top
            y_change -= MOVEMENT_DISTANCE_Y  # move up

    elif key_depressed == left:  # if left key is pressed
        if player.rect.x > 20:  # not at leftmost border
            x_change -= MOVEMENT_DISTANCE_X

    elif key_depressed == right:  # if right key is pressed
        if player.rect.x < 750:  # not at rightmost border
            x_change += MOVEMENT_DISTANCE_X

    elif key_depressed == down:  # if down key is pressed
        if player.rect.y < 800:  # not at bottom
            y_change += MOVEMENT_DISTANCE_Y

    player.rect.x += x_change
    player.rect.y += y_change


def main():
    """Main game method containing the main game loop"""
    log_game()
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))
    can_move = True

    # Initialize sprite groups
    render_group = pygame.sprite.RenderUpdates()
    kill_group = DeathSprites()
    win_group = pygame.sprite.Group()

    # Initialize sprites
    player = Player(asset_dict["frog"])
    player.add(render_group)
    Car(asset_dict["car1"]).add(render_group, kill_group)
    FrogNest(1).add(win_group)
    FrogNest(2).add(win_group)
    FrogNest(3).add(win_group)
    FrogNest(4).add(win_group)
    FrogNest(5).add(win_group)

    clock = pygame.time.Clock()
    run = True

    # Main game loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        # Input handling for movement
            if event.type == pygame.KEYDOWN and can_move:
                can_move = False
                key_depressed = event.key
                move_player(player, key_depressed)
            if event.type == pygame.KEYUP:
                can_move = True

        # Check collisions and render sprites on every frame
        check_kill_collisions(player, kill_group)
        check_win_collisions(player, win_group)
        draw_window(render_group)


if __name__ == "__main__":
    main()
