import unittest
import logging
from testfixtures import LogCapture
from src import main


class TestGameMethods(unittest.TestCase):

    def test_game_start(self):
        with self.assertLogs() as logs:
            main.main()
        self.assertEqual(logs.output, ["INFO:root:Welcome to The Froggerithm!"])