# File: main.py
# Authors: John Cooke, Zion Emond, Alex Stiner
# Since: 2/12/2021
# This file contains the main game loop and will initialize all the game systems
"""
This module will contain the main high level functions of the game, as well as the main game loop
"""
import os
import pygame
from Engine.logger import log_game
from Engine.sprite_renderer import draw_sprites
from Engine.movement_handler import move_player
from Engine.obstacle_spawner import spawn_water_lanes, spawn_car_lanes
from Util.utilities import check_kill_collisions, check_win_collisions
from Util.asset_dictionary import AssetDictionary
from Sprites.player import Player
from Sprites.car import Car
from Sprites.log import Log
from Sprites.frog_nest import FrogNest
from Sprites.Groups.death_sprites import DeathSprites


WIDTH, HEIGHT = 820, 876
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Froggerithm")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load background image
background_image = pygame.image.load(os.path.join(current_dir, "Assets", "background.png"))
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load assets into an object for easy access
asset_dict = AssetDictionary(current_dir)

MOVEMENT_DISTANCE_X = asset_dict.get_asset("frog").get_width() + 4
MOVEMENT_DISTANCE_Y = asset_dict.get_asset("frog").get_height() + 12

# Prepare images for player animation
player_images = [asset_dict.get_asset("frog"), asset_dict.get_asset("frog_jumping")]


def main():
    """Main game method containing the main game loop"""
    log_game()
    WIN.fill(WHITE)
    WIN.blit(background, (0, 0))
    frame_count = 0
    can_move = True

    # Initialize sprite groups
    render_group = pygame.sprite.LayeredUpdates()
    kill_group = DeathSprites()
    win_group = pygame.sprite.Group()

    # Initialize sprite groups for the water "lanes"
    water_lane1 = pygame.sprite.Group()
    water_lane2 = pygame.sprite.Group()
    water_lane3 = pygame.sprite.Group()
    water_lane4 = pygame.sprite.Group()
    water_lane5 = pygame.sprite.Group()

    # Initialize logs on the screen on game start
    Log(asset_dict.get_asset("log-short"), 779, 308).add(water_lane2, render_group)
    Log(asset_dict.get_asset("log-short"), 539, 308).add(water_lane2, render_group)
    Log(asset_dict.get_asset("log-short"), 299, 308).add(water_lane2, render_group)

    Log(asset_dict.get_asset("log-long"), 425, 244).add(water_lane3, render_group)

    Log(asset_dict.get_asset("log-short"), 119, 116).add(water_lane5, render_group)
    Log(asset_dict.get_asset("log-short"), 419, 116).add(water_lane5, render_group)
    Log(asset_dict.get_asset("log-short"), 719, 116).add(water_lane5, render_group)

    # Initialize sprite groups for the car lanes
    car_lane1 = pygame.sprite.Group()
    car_lane2 = pygame.sprite.Group()
    car_lane3 = pygame.sprite.Group()
    car_lane4 = pygame.sprite.Group()
    car_lane5 = pygame.sprite.Group()

    # Initialize the cars at start of game
    Car(asset_dict.get_asset("car1"), 0, 750, WIN).add(render_group, car_lane1, kill_group)
    Car(asset_dict.get_asset("car2"), 0, 700, WIN).add(render_group, car_lane2, kill_group)
    Car(asset_dict.get_asset("car3"), 0, 630, WIN).add(render_group, car_lane3, kill_group)
    Car(asset_dict.get_asset("car4"), 0, 560, WIN).add(render_group, car_lane4, kill_group)
    Car(asset_dict.get_asset("car2"), 0, 500, WIN).add(render_group, car_lane5, kill_group)

    # Initialize sprites for Frog
    player = Player(player_images, WIN)
    player.add(render_group)
    render_group.change_layer(player, 1)
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
                move_player(player, key_depressed, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, asset_dict)
                player.index = 1
                player.image = player.images[player.index]
            if event.type == pygame.KEYUP:
                can_move = True
                player.index = 0
                player.image = player.images[player.index]

        # Check collisions, render sprites, and spawn obstacles on every frame
        check_kill_collisions(player, kill_group)
        check_win_collisions(player, win_group)
        spawn_car_lanes(frame_count, car_lane1, car_lane2, car_lane3, car_lane4, car_lane5,
                        render_group, kill_group, asset_dict, WIN)
        spawn_water_lanes(frame_count, water_lane1, water_lane2, water_lane3, water_lane4, water_lane5,
                          render_group, asset_dict, WIN)
        draw_sprites(render_group, WIN, background)

        # Iterate the frame counter
        frame_count += 1


if __name__ == "__main__":
    main()
