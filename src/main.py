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
from Engine.sprite_animator import animate_sprites
from Sprites.Groups.river_sprites import RiverSprites
from Engine.gameover import game_over
from Util.utilities import check_kill_collisions, check_win_collisions, add_river_sprites_to_group,\
    add_player_to_water_lane
from Util.asset_dictionary import AssetDictionary
from Util.window import Window
from Sprites.player import Player
from Sprites.car import Car
from Sprites.log import Log
from Sprites.frog_nest import FrogNest
from Sprites.riverbank import Riverbank
from Sprites.turtle import Turtle
from Sprites.water import WaterSprite, RiverEdge
from Sprites.turtle_animated import TurtleSinker
from Sprites.Groups.death_sprites import DeathSprites
from Sprites.Groups.nests import DisabledNests

WIN = Window.WIN
pygame.display.set_caption("The Froggerithm")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load background image
background_image = pygame.image.load(os.path.join(current_dir, "Assets/Images", "background.png"))
background = pygame.transform.scale(background_image, (Window.WIDTH, Window.HEIGHT))

MOVEMENT_DISTANCE_X = AssetDictionary.get_asset("frog").get_width() + 4
MOVEMENT_DISTANCE_Y = AssetDictionary.get_asset("frog").get_height() + 12

start = True

def text_ob(text, font, color):
    textforScreen = font.render(text, True, color)
    return textforScreen, textforScreen.get_rect()

while start:
    """Initialize font before beginning of game"""
    pygame.font.init()

    """Start Screen"""
    blue = pygame.Color(0, 0, 255)
    aqua = pygame.Color(0, 255, 255)

    """"When mouse or key is pressed end Start Screen"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
         start = False

    """"Fill in Start Screen with color and text"""
    WIN.fill(BLACK)
    text = pygame.font.SysFont('Times New Roman', 100)
    Text, TextRect = text_ob("The Froggerithm", text, WHITE)
    text2 = pygame.font.SysFont('Times New Roman', 35)
    Text2, TextRect2 = text_ob("Click on the Screen to Start the Game", text2, aqua)
    TextRect.center = ((Window.WIDTH / 2), (Window.HEIGHT / 2))
    TextRect2.center = (((Window.WIDTH) / 2), ((Window.HEIGHT + 200) / 2))
    WIN.blit(Text, TextRect)
    WIN.blit(Text2, TextRect2)
    pygame.display.update()


def main():
    pygame.init()
    pygame.mixer.init()
    """Main game method containing the main game loop"""
    log_game()

    WIN.blit(background, (0, 0))
    frame_count = 0
    can_move = True

    # Load the sounds
    hop_sound = pygame.mixer.Sound("src/Assets/Sounds/hop.wav")
    pygame.mixer.music.load("src/Assets/Sounds/Frogger_music.mp3")
    pygame.mixer.music.play(-1)  # Loops the music indefinitely

    # Initialize on-screen text
    pygame.font.init()
    frogger_font = pygame.font.SysFont("Consolas", 30)

    # Initialize sprite groups
    render_group = pygame.sprite.LayeredUpdates()
    kill_group = DeathSprites()
    win_group = pygame.sprite.Group()
    disabled_nests = DisabledNests()
    river_group = RiverSprites()

    # Initialize sprite groups for the water "lanes"
    water_lane1 = pygame.sprite.Group()
    water_lane2 = pygame.sprite.Group()
    water_lane3 = pygame.sprite.Group()
    water_lane4 = pygame.sprite.Group()
    water_lane5 = pygame.sprite.Group()
    water_lanes = [water_lane1, water_lane2, water_lane3, water_lane4, water_lane5]

    # Initialize logs and turtles already on the screen at game start
    Log(AssetDictionary.get_asset("log-short"), 779, 308).add(water_lane2, render_group)
    Log(AssetDictionary.get_asset("log-short"), 539, 308).add(water_lane2, render_group)
    Log(AssetDictionary.get_asset("log-short"), 299, 308).add(water_lane2, render_group)

    TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), -30, -79, 372).add(water_lane1, render_group)
    Turtle(AssetDictionary.get_asset("triple-turtle"), frame_count, 221, 372).add(water_lane1, render_group)
    Turtle(AssetDictionary.get_asset("triple-turtle"), frame_count, 521, 372).add(water_lane1, render_group)

    Log(AssetDictionary.get_asset("log-long"), 425, 244).add(water_lane3, render_group)

    TurtleSinker(AssetDictionary.get_asset("double-turtle-sink"), -30, 0, 180).add(water_lane4, render_group)
    Turtle(AssetDictionary.get_asset("double-turtle"), frame_count, 270, 180).add(water_lane4, render_group)
    Turtle(AssetDictionary.get_asset("double-turtle"), frame_count, 540, 180).add(water_lane4, render_group)

    Log(AssetDictionary.get_asset("log-medium"), 219, 116).add(water_lane5, render_group)
    Log(AssetDictionary.get_asset("log-medium"), 719, 116).add(water_lane5, render_group)

    # Initialize sprite groups for the car lanes
    car_lane1 = pygame.sprite.Group()
    car_lane2 = pygame.sprite.Group()
    car_lane3 = pygame.sprite.Group()
    car_lane4 = pygame.sprite.Group()
    car_lane5 = pygame.sprite.Group()

    # Initialize the cars at start of game
    Car(AssetDictionary.get_asset("car4"), WIN.get_width() - 500, 750, WIN).add(render_group, car_lane1, kill_group)
    Car(AssetDictionary.get_asset("car4"), WIN.get_width() - 260, 750, WIN).add(render_group, car_lane1, kill_group)
    Car(AssetDictionary.get_asset("car3"), 660, 700, WIN).add(render_group, car_lane2, kill_group)
    Car(AssetDictionary.get_asset("car3"), 300, 700, WIN).add(render_group, car_lane2, kill_group)
    Car(AssetDictionary.get_asset("car2"), WIN.get_width() - 400, 630, WIN).add(render_group, car_lane3, kill_group)
    Car(AssetDictionary.get_asset("semi-truck"), WIN.get_width() - 360, 500, WIN).add(
        render_group, car_lane5, kill_group)

    # Initialize sprites for Frog
    player = Player(AssetDictionary.get_asset("player"))
    player.add(render_group)
    render_group.change_layer(player, 1)
    FrogNest(1).add(win_group)
    FrogNest(2).add(win_group)
    FrogNest(3).add(win_group)
    FrogNest(4).add(win_group)
    FrogNest(5).add(win_group)

    # Initialize sprites for Riverbank
    Riverbank(0).add(kill_group)
    Riverbank(1).add(kill_group)
    Riverbank(2).add(kill_group)
    Riverbank(3).add(kill_group)
    Riverbank(4).add(kill_group)
    Riverbank(5).add(kill_group)

    # Initialize sprites for WaterSprite
    river = WaterSprite()
    river.add(river_group)

    # Initialize sprites on the edges of the river for checking if the player is offscreen
    RiverEdge("left").add(kill_group)
    RiverEdge("right").add(kill_group)

    clock = pygame.time.Clock()

    # Create counter, timer and fonts for timer, counter
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    text = pygame.font.SysFont('Times New Roman', 35)

    run = True

     # Main game loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Timer for player to complete game
            if event.type == pygame.USEREVENT:
                Window.TIMER -= 1

                # if the timer has hit zero, kill the player and restart it
                if Window.TIMER < 1:
                    player.kill()

                else:
                    Window.TIMER_TEXT = str(Window.TIMER).rjust(5)

        # Input handling for movement
            if event.type == pygame.KEYDOWN and can_move:
                can_move = False
                key_depressed = event.key
                move_player(player, key_depressed, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, hop_sound)
                player.index = 1
                player.image = player.images[player.index]
            if event.type == pygame.KEYUP:
                can_move = True
                player.index = 0
                player.image = player.images[player.index]

        text_timer_box = text.render(Window.TIMER_TEXT, True, (255, 255, 255))

        # Check collisions, render & animate sprites, and spawn obstacles on every frame
        check_kill_collisions(player, kill_group)
        check_win_collisions(player, win_group, render_group, kill_group, disabled_nests)
        spawn_car_lanes(frame_count, car_lane1, car_lane2, car_lane3, car_lane4, car_lane5,
                        render_group, kill_group, WIN)
        spawn_water_lanes(frame_count, water_lane1, water_lane2, water_lane3, water_lane4, water_lane5,
                          render_group, WIN)
        animate_sprites(water_lane1, water_lane4, frame_count)
        draw_sprites(render_group, WIN, background, text_timer_box)
        add_river_sprites_to_group(water_lanes, river_group)
        river_group.check_if_sunk(player, river)
        add_player_to_water_lane(water_lanes, player)

        # Initialize and render score text
        score_text = frogger_font.render("Score: " + str(player.score), True, WHITE, BLACK)
        background.blit(score_text, (20, 10))

        # Initialize and render lives left
        lives_text = frogger_font.render("Lives: " + str(player.lives_left), True, WHITE, BLACK)
        background.blit(lives_text, (650, 10))

        # Iterate the frame counter
        frame_count += 1


if __name__ == "__main__":
    main()
    game_over()
