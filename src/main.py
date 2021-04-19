# File: main.py
# Authors: John Cooke, Zion Emond, Alex Stiner
# Since: 2/12/2021
# This file contains the main game loop and will initialize all the game systems
"""
This module will contain the main high level functions of the game, as well as the main game loop
"""
import os
import pygame
import pygame.locals
import sys
import neat
import pickle
from Engine.logger import log_game
from Engine.sprite_renderer import draw_sprites
from Engine.movement_handler import move_player
from Engine.obstacle_spawner import spawn_water_lanes, spawn_car_lanes
from Engine.sprite_animator import animate_sprites
from Sprites.Groups.river_sprites import RiverSprites
from Util.utilities import check_kill_collisions, check_win_collisions, add_sprites_to_group, \
    add_player_to_water_lane, parse_if_training_net, determine_keypress
from Engine.gameover import game_over
from Util.asset_dictionary import AssetDictionary
from Util.window import Window
from Util.timer import Timer
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
NEAT_CONFIG = os.path.join(current_dir, "neat_config.txt")
training_flag = parse_if_training_net(sys.argv)

# Load background image
background_image = pygame.image.load(os.path.join(current_dir, "Assets/Images", "background.png"))
background = pygame.transform.scale(background_image, (Window.WIDTH, Window.HEIGHT))

MOVEMENT_DISTANCE_X = AssetDictionary.get_asset("frog").get_width() + 4
MOVEMENT_DISTANCE_Y = AssetDictionary.get_asset("frog").get_height() + 12

def text_ob(text, font, color):
    textforscreen = font.render(text, True, color)
    return textforscreen, textforscreen.get_rect()


def start_screen():
    """
    Renders the start screen until the player clicks to start the game. Should only appear if the AI is not being trained.

    :return: None
    """
    start = True
    while start:
        # Initialize font before beginning of game
        pygame.font.init()

        # Start Screen
        blue = pygame.Color(0, 0, 255)
        aqua = pygame.Color(0, 255, 255)

        # When mouse or key is pressed end Start Screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start = False

        # Fill in Start Screen with color and text
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


def main(genomes="", config=""):
    """
    Main game method containing the main game loop. Also handles the logic regarding spawning in all of the
    players for a training generation and assessing their fitness.

    - :param genomes:
        Genomes passed in by NEAT-python library.
    - :param config:
        Configuration passed in by NEAT-python library.
    - :return:
        Exit code
    """

    if not training_flag:
        start_screen()

    timer = Timer()
    pygame.init()
    pygame.mixer.init()
    log_game()
    player_lines = []

    WIN.blit(background, (0, 0))
    frame_count = 0

    # Load the sounds
    if not training_flag:
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
    net_group = pygame.sprite.Group()  # A group used for any sprites we want the neural net to see

    # A list of sprite groups that all logs and turtles should go in
    log_turtle_groups = [render_group, net_group]
    # A list of sprite groups that all cars should go in
    car_groups = [render_group, net_group, kill_group]

    # Initialize sprite groups for the water "lanes"
    water_lane1 = pygame.sprite.Group()
    water_lane2 = pygame.sprite.Group()
    water_lane3 = pygame.sprite.Group()
    water_lane4 = pygame.sprite.Group()
    water_lane5 = pygame.sprite.Group()
    water_lanes = [water_lane1, water_lane2, water_lane3, water_lane4, water_lane5]

    # Initialize logs and turtles already on the screen at game start
    Log(AssetDictionary.get_asset("log-short"), 779, 308).add(water_lane2, log_turtle_groups)
    Log(AssetDictionary.get_asset("log-short"), 539, 308).add(water_lane2, log_turtle_groups)
    Log(AssetDictionary.get_asset("log-short"), 299, 308).add(water_lane2, log_turtle_groups)

    TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), -30, -79, 372).add(water_lane1, log_turtle_groups)
    Turtle(AssetDictionary.get_asset("triple-turtle"), frame_count, 221, 372).add(water_lane1, log_turtle_groups)
    Turtle(AssetDictionary.get_asset("triple-turtle"), frame_count, 521, 372).add(water_lane1, log_turtle_groups)

    Log(AssetDictionary.get_asset("log-long"), 425, 244).add(water_lane3, render_group, log_turtle_groups)

    TurtleSinker(AssetDictionary.get_asset("double-turtle-sink"), -30, 0, 180).add(water_lane4, log_turtle_groups)
    Turtle(AssetDictionary.get_asset("double-turtle"), frame_count, 270, 180).add(water_lane4, log_turtle_groups)
    Turtle(AssetDictionary.get_asset("double-turtle"), frame_count, 540, 180).add(water_lane4, log_turtle_groups)

    Log(AssetDictionary.get_asset("log-medium"), 219, 116).add(water_lane5, log_turtle_groups)
    Log(AssetDictionary.get_asset("log-medium"), 719, 116).add(water_lane5, log_turtle_groups)

    # Initialize sprite groups for the car lanes
    car_lane1 = pygame.sprite.Group()
    car_lane2 = pygame.sprite.Group()
    car_lane3 = pygame.sprite.Group()
    car_lane4 = pygame.sprite.Group()
    car_lane5 = pygame.sprite.Group()

    # Initialize the cars at start of game
    Car(AssetDictionary.get_asset("car4"), WIN.get_width() - 500, 750, WIN).add(car_lane1, car_groups)
    Car(AssetDictionary.get_asset("car4"), WIN.get_width() - 260, 750, WIN).add(car_lane1, car_groups)
    Car(AssetDictionary.get_asset("car3"), 660, 700, WIN).add(car_lane2, car_groups)
    Car(AssetDictionary.get_asset("car3"), 300, 700, WIN).add(car_lane2, car_groups)
    Car(AssetDictionary.get_asset("car2"), WIN.get_width() - 400, 630, WIN).add(car_lane3, car_groups)
    Car(AssetDictionary.get_asset("semi-truck"), WIN.get_width() - 360, 500, WIN).add(car_lane5, car_groups)

    # Initialize sprites for Frog
    # player = Player(render_group)
    FrogNest(1).add(win_group, net_group)
    FrogNest(2).add(win_group, net_group)
    FrogNest(3).add(win_group, net_group)
    FrogNest(4).add(win_group, net_group)
    FrogNest(5).add(win_group, net_group)

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
    timer_event = pygame.event.Event(pygame.USEREVENT, {})
    # pygame.time.set_timer(timer_event, 1000)

    # Initialize genomes and neural networks if flag is set
    if training_flag:
        nets = []
        players = []
        genome_list = []

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            players.append(Player(render_group))
            genome_list.append(genome)

    run = True

    # Main game loop
    while run:
        if not training_flag:  # If training the AI, let the game use all compute overhead
            clock.tick(FPS)
        max_lives = 0
        highest_score = 0
        # keypress = False
        # while not keypress:
        #     for game_event in pygame.event.get():
        #         if game_event.type == pygame.KEYDOWN:
        #             keypress = True

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                run = False

            # Timer for player to complete game
            if game_event == timer_event:
                timer.count_down()

        for i, player in enumerate(players):
            # Begin neural net logic
            genome_list[i].fitness = player.score

            # If the timer has hit zero, kill the player before letting it compute its move
            if timer.get_time() < 1:
                player.kill()

            # On every 10th frame, allow the neural net to move the frog
            if frame_count % 10 == 0:
                distance_to_sprite_ahead = player.find_distance_to_sprite("ahead", net_group, player_lines)
                distance_to_sprite_below = player.find_distance_to_sprite("down", net_group, player_lines)
                distance_to_left_sprite = player.find_distance_to_sprite("left", net_group, player_lines)
                distance_to_right_sprite = player.find_distance_to_sprite("right", net_group, player_lines)
                distance_in_lane_ahead = player.find_sprite_in_next_lane("ahead", net_group, player_lines)
                distance_in_lane_behind = player.find_sprite_in_next_lane("down", net_group, player_lines)

                frames_since_last_advancement = frame_count - player.last_advancement

                # Feed values to the neural net to compute the action to be taken on the current frame
                output = nets[players.index(player)].activate((player.rect.x, player.rect.y,
                                                               frames_since_last_advancement, distance_to_sprite_ahead,
                                                               distance_to_sprite_below, distance_to_left_sprite,
                                                               distance_to_right_sprite, player.on_sinking_turtle,
                                                               distance_in_lane_ahead[0], distance_in_lane_ahead[1],
                                                               distance_in_lane_behind[0], distance_in_lane_behind[1],
                                                               len(player.disabled_nests.sprites())))

                # If no node in the output layer is greater than 0.5, the player will do nothing on this frame
                if max(output) > 0.5:
                    max_node_index = output.index(max(output))

                    # Move the player based on the output of the neural net
                    key_to_press = determine_keypress(max_node_index)
                    player.move(key_to_press, frame_count)

            # If the player hasn't moved for 10 seconds or more, kill it
            if frames_since_last_advancement >= 300:
                player.kill()
            # End neural net logic

            # Handle player logic that does not involve neural net
            check_kill_collisions(player, kill_group)
            check_win_collisions(player, win_group, render_group, kill_group, disabled_nests, timer)
            river_group.check_if_sunk(player, river)
            add_player_to_water_lane(water_lanes, player)
            player.set_score()
            animate_sprites(water_lane1, water_lane4, frame_count, net_group)

            # Input handling for movement
            # for game_event in pygame.event.get():
            #     if game_event.type == pygame.KEYDOWN and player.can_move:
            #         player.can_move = False
            #         key_depressed = game_event.key
            #         move_player(player, key_depressed, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
            #         player.index = 1
            #         player.image = player.images[player.index]
            #     if game_event.type == pygame.KEYUP:
            #         player.can_move = True
            #         player.index = 0
            #         player.image = player.images[player.index]

            if player.lives_left < 0:
                players.remove(player)
                nets.remove(nets[i])
                genome_list.remove(genome_list[i])

            if player.score > highest_score:
                highest_score = player.score

            if player.lives_left > max_lives:
                max_lives = player.lives_left

        # Handle all logic that does not involve the player that must be done on every frame
        spawn_car_lanes(frame_count, car_lane1, car_lane2, car_lane3, car_lane4, car_lane5,
                        car_groups, WIN)
        spawn_water_lanes(frame_count, water_lane1, water_lane2, water_lane3, water_lane4, water_lane5,
                          log_turtle_groups, WIN)
        add_sprites_to_group(water_lanes, river_group)
        draw_sprites(render_group, WIN, background)

        # Initialize and render score text
        empty_text = frogger_font.render("Score: 00000", True, BLACK, BLACK)
        background.blit(empty_text, (20, 10))
        score_text = frogger_font.render("Score: " + str(int(highest_score)), True, WHITE, BLACK)
        background.blit(score_text, (20, 10))

        # Initialize and render lives left
        lives_text = frogger_font.render("Lives: " + str(max_lives), True, WHITE, BLACK)
        background.blit(lives_text, (650, 10))

        # Initialize and render timer
        empty_text = frogger_font.render("Time: 00", True, BLACK, BLACK)
        background.blit(empty_text, (355, 10))
        timer_text = frogger_font.render("Time: " + str(timer.get_time()), True, WHITE, BLACK)
        background.blit(timer_text, (355, 10))

        if len(players) <= 0:
            run = False

        # Iterate the frame counter
        frame_count += 1

        if timer.get_time() < 1:
            timer.reset()

        # Push a timer event to the event queue every second to iterate the timer
        if frame_count % FPS == 0:
            pygame.event.post(timer_event)


def run_neat(generations):
    """
    This function contains the NEAT-python objects which are used to train and run the AI. It sets up the objects
    and then calls main to run the NEAT training algorithm for the number of generations specified in the CLI.

    - :param generations:
        An int representing the number of generations the neural network should be trained for.
    - :return:
        None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, NEAT_CONFIG)

    population = neat.Population(config)
    # Uncomment the next line to load a checkpoint, change the number after 'neat-checkpoint-' to whichever checkpoint number you wish to load
    # population = neat.checkpoint.Checkpointer.restore_checkpoint(os.path.join(current_dir, 'Checkpoints', 'neat-checkpoint-674'))
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    checkpoint_file = os.path.join(current_dir, 'Checkpoints', 'neat-checkpoint-')
    checkpointer = neat.checkpoint.Checkpointer(100, 1200, checkpoint_file)
    population.add_reporter(checkpointer)

    best = population.run(main, int(generations))
    # If a genome reached our fitness threshold, save it to a file on disk
    save_path = os.path.join(current_dir, 'best-genome.txt')
    with open(save_path, 'wb+') as file:
        pickle.dump(best, file)

    print('\nBest genome:\n{!s}'.format(best))


if __name__ == "__main__":
    if training_flag:
        run_neat(training_flag)
    else:
        main()
        game_over()
