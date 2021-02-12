# File: game_tests.py
# Authors: John Cooke
# Since: 2/12/2021
# This file contains all the unit tests for the main functions of the game
"""Contains all the unit tests for the main functions of the game"""
import unittest
from src import main


class TestGameMethods(unittest.TestCase):
    """Contains the main game unit testing methods"""

    def test_game_start(self):
        """Tests whether the game starts by checking the console logs"""
        with self.assertLogs() as logs:
            main.main()
        self.assertEqual(logs.output, ["INFO:root:Welcome to The Froggerithm!"])
