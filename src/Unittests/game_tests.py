# File: game_tests.py
# Authors: John Cooke, Zion Emond, Alex Stiner
# Since: 2/12/2021
# This file contains all the unit tests for the main functions of the game
"""Contains all the unit tests for the main functions of the game"""
import unittest
import pygame
import Engine.obstacle_spawner as obstacle_spawner
from Sprites.Groups.death_sprites import DeathSprites
from Sprites.car import Car
import Engine.sprite_animator as sprite_animator
from Sprites.frog_nest import FrogNest
from Util.asset_dictionary import AssetDictionary
from Util.window import Window
from Sprites.turtle import Turtle
from Sprites.turtle_animated import TurtleSinker
from Sprites.log import Log
from Sprites.player import Player
from Sprites.Groups.nests import DisabledNests
from Engine.movement_handler import move_player


class TestGameMethods(unittest.TestCase):
    """Contains the main game unit testing methods"""

    def test_sprite_despawner(self):
        test_win = pygame.Surface((820, 876))
        test_sprite = Log(AssetDictionary.get_asset("log-short"), 100, 100)
        test_group = pygame.sprite.Group()

        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertTrue(test_group.has(test_sprite))

        test_sprite.rect.x = 0 - test_sprite.image.get_width() - 1
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

        test_sprite.rect.x = 825
        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

        test_sprite.rect.y = 0 - test_sprite.image.get_height() - 1
        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

        test_sprite.rect.y = test_win.get_height() + 1
        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

        test_sprite.rect.x = 481856
        test_sprite.rect.y = 156135
        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

        test_sprite.rect.x = -748964
        test_sprite.rect.y = -156489
        test_group.add(test_sprite)
        obstacle_spawner.sprite_despawner(test_sprite, test_win)
        self.assertFalse(test_group.has(test_sprite))

    def test_water_spawner(self):
        test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                      pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # test that all lanes spawn properly
        obstacle_spawner.spawn_water_lanes(0, test_lanes[0], test_lanes[1], test_lanes[2], test_lanes[3], test_lanes[4],
                                           test_render_group, test_win)

        Turtle(AssetDictionary.get_asset("triple-turtle"), 0, 816, 372).add(assert_groups[0])
        Log(AssetDictionary.get_asset("log-short"), -180, 308).add(assert_groups[1])
        Log(AssetDictionary.get_asset("log-long"), -377, 244).add(assert_groups[2])
        Turtle(AssetDictionary.get_asset("double-turtle"), 0, 817, 180).add(assert_groups[3])
        Log(AssetDictionary.get_asset("log-medium"), -278, 116).add(assert_groups[4])

        for test_lane, assert_group in zip(test_lanes, assert_groups):
            for i, j in zip(test_lane.sprites(), assert_group.sprites()):
                self.assertEqual(i.rect.x, j.rect.x)
                self.assertEqual(i.rect.y, j.rect.y)
            assert_group.empty()
            test_lane.empty()

        test_render_group.empty()

    def test_water_mover(self):

        test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                      pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # actual sprites
        Turtle(AssetDictionary.get_asset("triple-turtle"), 0, 300, 308).add(assert_groups[0], test_render_group)

        Log(AssetDictionary.get_asset("log-short"), 779, 308).add(test_lanes[1], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 539, 308).add(test_lanes[1], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 299, 308).add(test_lanes[1], test_render_group)

        Log(AssetDictionary.get_asset("log-long"), 425, 244).add(test_lanes[2], test_render_group)

        Turtle(AssetDictionary.get_asset("double-turtle"), 0, 121, 308).add(test_lanes[3], test_render_group)
        Turtle(AssetDictionary.get_asset("double-turtle"), 0, 625, 308).add(test_lanes[3], test_render_group)

        Log(AssetDictionary.get_asset("log-short"), 119, 116).add(test_lanes[4], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 419, 116).add(test_lanes[4], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 719, 116).add(test_lanes[4], test_render_group)

        # expected sprites
        Turtle(AssetDictionary.get_asset("triple-turtle"), 0, 305, 308).add(assert_groups[0], test_render_group)

        Log(AssetDictionary.get_asset("log-short"), 780, 308).add(assert_groups[1], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 540, 308).add(assert_groups[1], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 300, 308).add(assert_groups[1], test_render_group)

        Log(AssetDictionary.get_asset("log-long"), 433, 244).add(assert_groups[2], test_render_group)

        Turtle(AssetDictionary.get_asset("double-turtle"), 0, 117, 308).add(assert_groups[3], test_render_group)
        Turtle(AssetDictionary.get_asset("double-turtle"), 0, 621, 308).add(assert_groups[3], test_render_group)

        Log(AssetDictionary.get_asset("log-short"), 122, 116).add(assert_groups[4], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 422, 116).add(assert_groups[4], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 722, 116).add(assert_groups[4], test_render_group)

        # call function on actual sprites and test it
        obstacle_spawner.spawn_water_lanes(12, test_lanes[0], test_lanes[1], test_lanes[2], test_lanes[3],
                                           test_lanes[4], test_render_group, test_win)

        for test_lane, assert_group in zip(test_lanes, assert_groups):
            for i, j in zip(test_lane.sprites(), assert_group.sprites()):
                self.assertEqual(i.rect.x, j.rect.x)
                self.assertEqual(i.rect.y, j.rect.y)
            assert_group.empty()
            test_lane.empty()

        test_render_group.empty()

    def test_water_despawner(self):

        test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                      pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # actual sprites
        Turtle(AssetDictionary.get_asset("triple-turtle"), 0, -100, 308).add(assert_groups[0], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 877, 308).add(test_lanes[1], test_render_group)
        Log(AssetDictionary.get_asset("log-long"), 900, 244).add(test_lanes[2], test_render_group)
        Turtle(AssetDictionary.get_asset("double-turtle"), 0, -50, 308).add(test_lanes[3], test_render_group)
        Log(AssetDictionary.get_asset("log-short"), 1050, 116).add(test_lanes[4], test_render_group)

        # call function on the actual sprites and test
        obstacle_spawner.spawn_water_lanes(1, test_lanes[0], test_lanes[1], test_lanes[2], test_lanes[3], test_lanes[4],
                                           test_render_group, test_win)

        for lane in test_lanes:
            self.assertFalse(lane.has())

        test_render_group.empty()

    def test_animated_turtle(self):
        test_sinker = TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), 0, -79, 372, 1)

        self.assertFalse(test_sinker.animation_started)
        self.assertFalse(test_sinker.submerged)
        self.assertFalse(test_sinker.emerging)
        self.assertEqual(test_sinker.frame_index, 0)
        self.assertEqual(test_sinker.last_animation, 0)

        test_sinker.start_animation(1)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 1)
        self.assertEqual(test_sinker.last_animation, 1)

        test_sinker.next_frame(2)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 2)
        self.assertEqual(test_sinker.last_animation, 2)

        test_sinker.next_frame(3)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 3)
        self.assertEqual(test_sinker.last_animation, 3)

        test_sinker.next_frame(4)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 2)
        self.assertEqual(test_sinker.last_animation, 4)
        self.assertFalse(test_sinker.submerged)
        self.assertTrue(test_sinker.emerging)

        test_sinker.next_frame(5)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 1)
        self.assertEqual(test_sinker.last_animation, 5)
        self.assertFalse(test_sinker.submerged)
        self.assertTrue(test_sinker.emerging)

        test_sinker.next_frame(6)
        self.assertFalse(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 0)
        self.assertEqual(test_sinker.last_animation, 6)
        self.assertFalse(test_sinker.submerged)
        self.assertFalse(test_sinker.emerging)

    def test_turtle_animator(self):
        test_lanes = [pygame.sprite.Group(), pygame.sprite.Group()]
        test_frame_count = 29
        test_turtle_0 = TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), 0, -79, 372)
        test_turtle_1 = TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), 0, -79, 372)
        test_lanes[0].add(test_turtle_0)
        test_lanes[1].add(test_turtle_1)

        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)
        self.assertFalse(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 0)
        self.assertEqual(test_turtle_0.last_animation, 0)

        self.assertFalse(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 0)
        self.assertEqual(test_turtle_1.last_animation, 0)

        test_frame_count += 1
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 1)
        self.assertEqual(test_turtle_0.last_animation, 30)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 1)
        self.assertEqual(test_turtle_1.last_animation, 30)

        test_frame_count += 1
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 1)
        self.assertEqual(test_turtle_0.last_animation, 30)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 1)
        self.assertEqual(test_turtle_1.last_animation, 30)

        test_frame_count += 17
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 2)
        self.assertEqual(test_turtle_0.last_animation, 48)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 2)
        self.assertEqual(test_turtle_1.last_animation, 48)

        test_frame_count += 18
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertTrue(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 3)
        self.assertEqual(test_turtle_0.last_animation, 66)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertTrue(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 3)
        self.assertEqual(test_turtle_1.last_animation, 66)

        test_frame_count += 1
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertTrue(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 3)
        self.assertEqual(test_turtle_0.last_animation, 66)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertTrue(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 3)
        self.assertEqual(test_turtle_1.last_animation, 66)

        test_frame_count += 17
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertTrue(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 2)
        self.assertEqual(test_turtle_0.last_animation, 84)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertTrue(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 2)
        self.assertEqual(test_turtle_1.last_animation, 84)

        test_frame_count += 1
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertTrue(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 2)
        self.assertEqual(test_turtle_0.last_animation, 84)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertTrue(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 2)
        self.assertEqual(test_turtle_1.last_animation, 84)

        test_frame_count += 17
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertTrue(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertTrue(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 1)
        self.assertEqual(test_turtle_0.last_animation, 102)

        self.assertTrue(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertTrue(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 1)
        self.assertEqual(test_turtle_1.last_animation, 102)

        test_frame_count += 18
        sprite_animator.animate_turtles(test_lanes[0], test_lanes[1], test_frame_count)

        self.assertFalse(test_turtle_0.animation_started)
        self.assertFalse(test_turtle_0.submerged)
        self.assertFalse(test_turtle_0.emerging)
        self.assertEqual(test_turtle_0.frame_index, 0)
        self.assertEqual(test_turtle_0.last_animation, 120)

        self.assertFalse(test_turtle_1.animation_started)
        self.assertFalse(test_turtle_1.submerged)
        self.assertFalse(test_turtle_1.emerging)
        self.assertEqual(test_turtle_1.frame_index, 0)
        self.assertEqual(test_turtle_1.last_animation, 120)

    def test_player(self):
        pygame.init()
        actual = Player(AssetDictionary.get_asset("player"))

        actual.rect.x = 101
        actual.rect.y = 415
        actual.index = 1
        actual.direction = "right"

        expected = Player(AssetDictionary.get_asset("player"))

        actual.return_home()

        self.assertEqual(actual.rect.x, expected.rect.x)
        self.assertEqual(actual.rect.y, expected.rect.y)
        self.assertEqual(actual.index, expected.index)
        self.assertEqual(actual.direction, expected.direction)

        actual.farthest_distance = 265
        expected.score += 50 + 2 * Window.TIMER

        actual.nest()

        self.assertEqual(actual.farthest_distance, expected.farthest_distance)
        self.assertEqual(actual.score, expected.score)

        actual.win_game()
        expected.score += 1000

        self.assertEqual(actual.score, expected.score)

        actual.kill()
        expected.lives_left -= 1

        self.assertEqual(actual.lives_left, expected.lives_left)

    def test_nests_group(self):

        actual = DisabledNests()
        self.assertFalse(actual.check_for_win())

        actual.add(FrogNest(1))
        self.assertFalse(actual.check_for_win())

        actual.add(FrogNest(2))
        self.assertFalse(actual.check_for_win())

        actual.add(FrogNest(3))
        self.assertFalse(actual.check_for_win())

        actual.add(FrogNest(4))
        self.assertFalse(actual.check_for_win())

        actual.add(FrogNest(5))
        self.assertTrue(actual.check_for_win())

        actual.add(FrogNest(1))
        self.assertTrue(actual.check_for_win())

    def test_car_spawner(self):
        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_kill_group = DeathSprites()
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # test that all lanes spawn properly
        obstacle_spawner.spawn_car_lanes(0, car_test_lanes[0], car_test_lanes[1], car_test_lanes[2], car_test_lanes[3],
                                         car_test_lanes[4], test_kill_group, test_render_group, test_win)

        Car(AssetDictionary.get_asset("car1"), 819, 750, test_win).add(assert_groups[0])
        Car(AssetDictionary.get_asset("car2"), 817, 700, test_win).add(assert_groups[1])
        Car(AssetDictionary.get_asset("car3"), 818, 630, test_win).add(assert_groups[2])
        Car(AssetDictionary.get_asset("car4"), -57, 560, test_win).add(assert_groups[3])
        Car(AssetDictionary.get_asset("semi-truck"), 817, 500, test_win).add(assert_groups[4])

        for car_test_lanes, assert_group in zip(car_test_lanes, assert_groups):
            for i, j in zip(car_test_lanes.sprites(), assert_group.sprites()):
                self.assertEqual(i.rect.x, j.rect.x)
                self.assertEqual(i.rect.y, j.rect.y)
            assert_group.empty()
            car_test_lanes.empty()

        test_render_group.empty()

    def test_car_mover(self):

        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # actual sprites
        Car(AssetDictionary.get_asset("car1"), 800, 750, test_win).add(car_test_lanes[0], test_render_group)

        Car(AssetDictionary.get_asset("car2"), 800, 700, test_win).add(car_test_lanes[1], test_render_group)
        Car(AssetDictionary.get_asset("car3"), 800, 630, test_win).add(car_test_lanes[2], test_render_group)
        Car(AssetDictionary.get_asset("car4"), 800, 560, test_win).add(car_test_lanes[3], test_render_group)

        Car(AssetDictionary.get_asset("semi-truck"), 800, 500, test_win).add(car_test_lanes[4], test_render_group)

        # expected sprites
        Car(AssetDictionary.get_asset("car1"), 798, 750, test_win).add(assert_groups[0], test_render_group)

        Car(AssetDictionary.get_asset("car2"), 802, 700, test_win).add(assert_groups[1], test_render_group)
        Car(AssetDictionary.get_asset("car3"), 797, 630, test_win).add(assert_groups[2], test_render_group)
        Car(AssetDictionary.get_asset("car4"), 803, 560, test_win).add(assert_groups[3], test_render_group)

        Car(AssetDictionary.get_asset("semi-truck"), 796, 500, test_win).add(assert_groups[4], test_render_group)

        # call function for actual sprites and test it
        obstacle_spawner.spawn_car_lanes(10, car_test_lanes[0], car_test_lanes[1], car_test_lanes[2], car_test_lanes[3],
                                         car_test_lanes[4], test_render_group, AssetDictionary, test_win)

        for car_test_lanes, assert_group in zip(car_test_lanes, assert_groups):
            for i, j in zip(car_test_lanes.sprites(), assert_group.sprites()):
                self.assertEqual(i.rect.x, j.rect.x)
                self.assertEqual(i.rect.y, j.rect.y)
            assert_group.empty()
            car_test_lanes.empty()

        test_render_group.empty()

    def test_car_despawner(self):

        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = pygame.sprite.RenderUpdates()
        test_kill_group = DeathSprites()
        test_win = pygame.Surface((820, 876))

        # actual sprites
        Car(AssetDictionary.get_asset("car1"), 800, 750, test_win).add(car_test_lanes[0], test_render_group)

        Car(AssetDictionary.get_asset("car2"), 800, 700, test_win).add(car_test_lanes[1], test_render_group)
        Car(AssetDictionary.get_asset("car3"), 800, 630, test_win).add(car_test_lanes[2], test_render_group)
        Car(AssetDictionary.get_asset("car4"), 800, 560, test_win).add(car_test_lanes[3], test_render_group)

        Car(AssetDictionary.get_asset("semi-truck"), 800, 500, test_win).add(car_test_lanes[4], test_render_group)

        # call function on the actual sprites and test
        obstacle_spawner.spawn_car_lanes(1, car_test_lanes[0], car_test_lanes[1], car_test_lanes[2], car_test_lanes[3],
                                         car_test_lanes[4], test_render_group, test_kill_group, test_win)

        for lane in car_test_lanes:
            self.assertFalse(lane.has())

        test_render_group.empty()

    def test_move_player(self):
        """Test whether the movement system works as expected"""
        test_player_images = [AssetDictionary.get_asset("frog"), AssetDictionary.get_asset("frog_jumping")]
        test_player = Player(test_player_images)
        up = 119  # 'w' key ascii
        left = 97  # 'a' key ascii
        right = 100  # 'd' key ascii
        down = 115  # 's' key ascii

        MOVEMENT_DISTANCE_X = AssetDictionary.get_asset("frog").get_width() + 4
        MOVEMENT_DISTANCE_Y = AssetDictionary.get_asset("frog").get_height() + 12

        # Test move up
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, up, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.y, 400 - MOVEMENT_DISTANCE_Y)

        # Test move left
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, left, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.x, 400 - MOVEMENT_DISTANCE_X)

        # Test move right
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, right, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.x, 400 + MOVEMENT_DISTANCE_X)

        # Test move down
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, down, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.y, 400 + MOVEMENT_DISTANCE_Y)

        # Test move left if player is at left edge
        test_player.rect.x = 20
        test_player.rect.y = 400
        move_player(test_player, left, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.x, 20)

        # Test move right if player is at right edge
        test_player.rect.x = 750
        test_player.rect.y = 400
        move_player(test_player, right, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.x, 750)

        # Test move up if player is at top edge
        test_player.rect.x = 400
        test_player.rect.y = 20
        move_player(test_player, up, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.y, 20)

        # Test move down if player is at bottom edge
        test_player.rect.x = 800
        test_player.rect.y = 400
        move_player(test_player, down, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y)
        self.assertEqual(test_player.rect.x, 800)
