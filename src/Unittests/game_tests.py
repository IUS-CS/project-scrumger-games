# File: game_tests.py
# Authors: John Cooke
# Since: 2/12/2021
# This file contains all the unit tests for the main functions of the game
"""Contains all the unit tests for the main functions of the game"""
import unittest
import pygame
import os
from src.Sprites.player import Player
from src.Engine.movement_handler import move_player
from src.Util.asset_dictionary import AssetDictionary

WIDTH, HEIGHT = 820, 876
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
current_dir = os.path.dirname(os.path.abspath(__file__))

asset_dict = AssetDictionary(current_dir)

MOVEMENT_DISTANCE_X = asset_dict.get_asset("frog").get_width() + 4
MOVEMENT_DISTANCE_Y = asset_dict.get_asset("frog").get_height() + 12


class TestGameMethods(unittest.TestCase):
    """Contains the main game unit testing methods"""

    # def test_game_start(self):
    #     """Tests whether the game starts by checking the console logs"""
    #     with self.assertLogs() as logs:
    #         main.main()
    #     self.assertEqual(logs.output, ["INFO:root:Welcome to The Froggerithm!"])

    def test_move_player(self):
        """Test whether the movement system works as expected"""
        test_player = Player(asset_dict.get_asset("frog"), WIN)
        up = 119  # 'w' key ascii
        left = 97  # 'a' key ascii
        right = 100  # 'd' key ascii
        down = 115  # 's' key ascii

        # Test move up
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, up)
        self.assertEqual(test_player.rect.y, 400 - MOVEMENT_DISTANCE_Y)

        # Test move left
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, left)
        self.assertEqual(test_player.rect.x, 400 - MOVEMENT_DISTANCE_X)

        # Test move right
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, right)
        self.assertEqual(test_player.rect.x, 400 + MOVEMENT_DISTANCE_X)

        # Test move down
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, down)
        self.assertEqual(test_player.rect.y, 400 + MOVEMENT_DISTANCE_Y)

        # Test move left if player is at left edge
        test_player.rect.x = 20
        test_player.rect.y = 400
        move_player(test_player, left)
        self.assertEqual(test_player.rect.x, 20)

        # Test move right if player is at right edge
        test_player.rect.x = 750
        test_player.rect.y = 400
        move_player(test_player, right)
        self.assertEqual(test_player.rect.x, 750)

        # Test move up if player is at top edge
        test_player.rect.x = 400
        test_player.rect.y = 20
        move_player(test_player, up)
        self.assertEqual(test_player.rect.y, 20)

        # Test move down if player is at bottom edge
        test_player.rect.x = 800
        test_player.rect.y = 400
        move_player(test_player, down)
        self.assertEqual(test_player.rect.x, 800)


