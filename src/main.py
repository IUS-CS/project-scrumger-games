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
FPS = 30
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

    def __init__(self, image, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = (WIDTH - self.rect.width) + x
        self.rect.y = y


class Log(pygame.sprite.Sprite):
    """Pygame sprite class representing a log floating in the river"""

    def __init__(self, image, initial_x,  initial_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.y = initial_y
        self.set_x(initial_x)

    def set_x(self, x):
        if x == -999:
            self.rect.x = -1 - self.image.get_width()
        else:
            self.rect.x = x

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
    "car3": pygame.image.load(os.path.join(current_dir, "Assets", "car-3.png")),
    "car4": pygame.image.load(os.path.join(current_dir, "Assets", "car-4.png")),
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


def spawn_water_lanes(framecount, lane1, lane2, lane3, lane4, lane5, render_group):
    """Handle spawning water platforms"""

    # Spawns logs in lane 2 every 8 seconds, skipping every 4th spawn
    if framecount == 0 or (framecount % 240 == 0 and framecount % 960 != 0):
        Log(asset_dict["log-short"], -999, 308).add(lane2, render_group)

    # Spawns logs in lane 3 every 9 seconds
    if framecount % 270 == 0:
        Log(asset_dict["log-long"], -999, 244).add(lane3, render_group)

    # Spawns logs in lane 5 every 5 seconds
    if framecount % 150 == 0:
        Log(asset_dict["log-short"], -999, 116).add(lane5, render_group)

    lane1_sprites = lane1.sprites()
    lane2_sprites = lane2.sprites()
    lane3_sprites = lane3.sprites()
    lane4_sprites = lane4.sprites()
    lane5_sprites = lane5.sprites()

    # Moves all entities in lane 2 at a constant speed and kill them if they have moved offscreen
    for sprite in lane2_sprites:
        sprite.rect.x += 1
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all entities in lane 3 at a constant speed and kill them if they have moved offscreen
    for sprite in lane3_sprites:
        sprite.rect.x += 3
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all entities in lane 5 at a constant speed and kill them if they have moved offscreen
    for sprite in lane5_sprites:
        sprite.rect.x += 2
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

def spawn_car_lanes(framecount, carlane1, carlane2, carlane3, carlane4, carlane5, render_group, kill_group):
    """Handle spawning car platforms"""
    # Spawns cars  in lane 1 every 8 seconds
    if framecount % 240 == 0:
        Car(asset_dict["car1"], 0, 750).add(carlane1, render_group, kill_group)

    # Spawns cars in lane 2 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict["car2"], 0, 700).add(carlane2, render_group, kill_group)

    # Spawns cars in lane 3 every 5 seconds
    if framecount % 150 == 0:
        Car(asset_dict["car3"], 0, 630).add(carlane3, render_group, kill_group)

    # Spawns cars  in lane 4 every 8 seconds
    if framecount % 240 == 0:
        Car(asset_dict["car4"], 0, 560).add(carlane4, render_group, kill_group)

    # Spawns cars in lane 5 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict["car2"], 0, 500).add(carlane5, render_group, kill_group)

    carlane1_sprites = carlane1.sprites()
    carlane2_sprites = carlane2.sprites()
    carlane3_sprites = carlane3.sprites()
    carlane4_sprites = carlane4.sprites()
    carlane5_sprites = carlane5.sprites()

    # Moves all cars in lane 1 at a constant speed and kill if go off screen
    for sprite in carlane1_sprites:
        sprite.rect.x += -1
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all cars in lane 2 at a constant speed and kill if go off screen
    for sprite in carlane2_sprites:
        sprite.rect.x += -3
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all cars in lane 3 at a constant speed and kill if go off screen
    for sprite in carlane3_sprites:
        sprite.rect.x += -2
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all cars in lane 4 at a constant speed and kill if go off screen
    for sprite in carlane4_sprites:
        sprite.rect.x += -1
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

    # Moves all cars in lane 5 at a constant speed and kill if go off screen
    for sprite in carlane5_sprites:
        sprite.rect.x += -3
        if sprite.rect.x > WIDTH + 1:
            sprite.kill()

def main():
    """Main game method containing the main game loop"""
    log_game()
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))
    frame_count = 0
    can_move = True

    # Initialize sprite groups
    render_group = pygame.sprite.RenderUpdates()
    kill_group = DeathSprites()
    win_group = pygame.sprite.Group()

    # Initialize sprite groups for the water "lanes"
    water_lane1 = pygame.sprite.Group()
    water_lane2 = pygame.sprite.Group()
    water_lane3 = pygame.sprite.Group()
    water_lane4 = pygame.sprite.Group()
    water_lane5 = pygame.sprite.Group()

    # Initialize logs on the screen on game start
    Log(asset_dict["log-short"], 779, 308).add(water_lane2, render_group)
    Log(asset_dict["log-short"], 539, 308).add(water_lane2, render_group)
    Log(asset_dict["log-short"], 299, 308).add(water_lane2, render_group)

    Log(asset_dict["log-long"], 425, 244).add(water_lane3, render_group)

    Log(asset_dict["log-short"], 119, 116).add(water_lane5, render_group)
    Log(asset_dict["log-short"], 419, 116).add(water_lane5, render_group)
    Log(asset_dict["log-short"], 719, 116).add(water_lane5, render_group)

    # Initialize sprite groups for the car lanes
    car_lane1 = pygame.sprite.Group()
    car_lane2 = pygame.sprite.Group()
    car_lane3 = pygame.sprite.Group()
    car_lane4 = pygame.sprite.Group()
    car_lane5 = pygame.sprite.Group()

    # Initialize the cars at start of game
    Car(asset_dict["car1"], 0, 750).add(render_group, car_lane1, kill_group)
    Car(asset_dict["car2"], 0, 700).add(render_group, car_lane2, kill_group)
    Car(asset_dict["car3"], 0, 630).add(render_group, car_lane3, kill_group)
    Car(asset_dict["car4"], 0, 560).add(render_group, car_lane4, kill_group)
    Car(asset_dict["car2"], 0, 500).add(render_group, car_lane5, kill_group)

    # Initialize sprites for Frog
    player = Player(asset_dict["frog"])
    player.add(render_group)
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

        # Check collisions, render sprites, and spawn obstacles on every frame
        check_kill_collisions(player, kill_group)
        check_win_collisions(player, win_group)
        spawn_car_lanes(frame_count, car_lane1, car_lane2, car_lane3, car_lane4, car_lane5, render_group, kill_group)
        spawn_water_lanes(frame_count, water_lane1, water_lane2, water_lane3, water_lane4, water_lane5, render_group)
        draw_window(render_group)

        # Iterate the frame counter
        frame_count += 1


if __name__ == "__main__":
    main()
