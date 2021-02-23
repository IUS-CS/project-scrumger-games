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
MOVEMENT_VELOCITY = 5
current_dir = os.path.dirname(os.path.abspath(__file__))


class Player(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - self.rect.height - 5


class Car(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH - self.rect.width
        self.rect.y = 700


class FrogNest(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([74, 50])
        self.image.fill(WHITE)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.set_pos(pos)

    def set_pos(self, pos):
        if pos == 1:
            self.rect.x = 45
            self.rect.y = 30

        elif pos == 2:
            self.rect.x = 205
            self.rect.y = 30

        elif pos == 3:
            self.rect.x = 365
            self.rect.y = 30

        elif pos == 4:
            self.rect.x = 525
            self.rect.y = 30

        else:
            self.rect.x = 685
            self.rect.y = 30


class DeathSprites(pygame.sprite.Group):

    def __init__(self):
        pygame.sprite.Group.__init__(self)


# Image scaling function for all assets
def scale_image(image):
    return pygame.transform.scale(image, (image.get_width()*4, image.get_height()*4))


# Stub method to be called when the player wins the game
def win_game():
    print("YOU WIN!")


# Checks the player sprite object against a group object
# and kills the sprite if it collides with any sprite in the group
def check_kill_collisions(player, kill_group):
    collide_list = pygame.sprite.spritecollide(player, kill_group, 0)
    if collide_list:
        player.kill()


# Checks the player sprite object against a group object for the game's win condition
def check_win_collisions(player, win_group):
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

MOVEMENT_DISTANCE_X = frog.get_width() + 4
MOVEMENT_DISTANCE_Y = frog.get_height() + 12


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



def move_player(player, keys_depressed):
    """Handles player movement"""

    # Make sure the player doesn't move off screen


    x_change = 0
    y_change = 0

    if keys_depressed[pygame.K_LEFT] or keys_depressed[pygame.K_a]:  # Left arrow key or a
        x_change -= MOVEMENT_DISTANCE_X

    elif keys_depressed[pygame.K_RIGHT] or keys_depressed[pygame.K_d]:  # Right arrow key or d
        x_change += MOVEMENT_DISTANCE_X

    elif keys_depressed[pygame.K_UP] or keys_depressed[pygame.K_w]:  # Up arrow key or w
        y_change -= MOVEMENT_DISTANCE_Y

    elif keys_depressed[pygame.K_DOWN] or keys_depressed[pygame.K_s]:  # Down arrow key or s
        y_change += MOVEMENT_DISTANCE_Y

    player.x += x_change
    player.y += y_change


def main():
    """Main game method containing the main game loop"""
    log_game()
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))

    # Initialize sprite groups
    render_group = pygame.sprite.RenderUpdates()
    kill_group = DeathSprites()
    win_group = pygame.sprite.Group()

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
        keys_depressed = pygame.key.get_pressed()

        if keys_depressed[pygame.K_LEFT] or keys_depressed[pygame.K_a]:  # Left arrow key or a
            player.rect.x -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_RIGHT] or keys_depressed[pygame.K_d]:  # Right arrow key or d
            player.rect.x += MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_UP] or keys_depressed[pygame.K_w]:  # Up arrow key or w
            player.rect.y -= MOVEMENT_VELOCITY

        if keys_depressed[pygame.K_DOWN] or keys_depressed[pygame.K_s]:  # Down arrow key or s
            player.rect.y += MOVEMENT_VELOCITY

        check_kill_collisions(player, kill_group)
        check_win_collisions(player, win_group)
        draw_window(render_group)
            if event.type == pygame.KEYDOWN:
                keys_depressed = pygame.key.get_pressed()
                move_player(player, keys_depressed)


if __name__ == "__main__":
    main()
