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
from Util.window import Window
import Engine.sprite_animator as sprite_animator
from Sprites.frog_nest import FrogNest
from Util.asset_dictionary import AssetDictionary
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
        test_net_group = pygame.sprite.Group()
        test_sinker = TurtleSinker(AssetDictionary.get_asset("triple-turtle-sink"), 0, -79, 372, 1)
        test_net_group.add(test_sinker)

        self.assertFalse(test_sinker.animation_started)
        self.assertFalse(test_sinker.submerged)
        self.assertFalse(test_sinker.emerging)
        self.assertEqual(test_sinker.frame_index, 0)
        self.assertEqual(test_sinker.last_animation, 0)

        test_sinker.start_animation(1, test_net_group)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 1)
        self.assertEqual(test_sinker.last_animation, 1)
        self.assertTrue(test_net_group.has(test_sinker))

        test_sinker.next_frame(2, test_net_group)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 2)
        self.assertEqual(test_sinker.last_animation, 2)
        self.assertTrue(test_net_group.has(test_sinker))

        test_sinker.next_frame(3, test_net_group)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 3)
        self.assertEqual(test_sinker.last_animation, 3)
        self.assertTrue(test_sinker.submerged)
        self.assertFalse(test_net_group.has(test_sinker))

        test_sinker.next_frame(4, test_net_group)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 2)
        self.assertEqual(test_sinker.last_animation, 4)
        self.assertFalse(test_sinker.submerged)
        self.assertTrue(test_sinker.emerging)
        self.assertTrue(test_net_group.has(test_sinker))

        test_sinker.next_frame(5, test_net_group)
        self.assertTrue(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 1)
        self.assertEqual(test_sinker.last_animation, 5)
        self.assertFalse(test_sinker.submerged)
        self.assertTrue(test_sinker.emerging)
        self.assertTrue(test_net_group.has(test_sinker))

        test_sinker.next_frame(6, test_net_group)
        self.assertFalse(test_sinker.animation_started)
        self.assertEqual(test_sinker.frame_index, 0)
        self.assertEqual(test_sinker.last_animation, 6)
        self.assertFalse(test_sinker.submerged)
        self.assertFalse(test_sinker.emerging)
        self.assertTrue(test_net_group.has(test_sinker))

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
        test_render_group = pygame.sprite.LayeredUpdates()
        actual = Player(test_render_group)
        test_timer = 20
        nest = FrogNest(1)

        actual.rect.x = 101
        actual.rect.y = 415
        actual.index = 1
        actual.direction = "right"

        expected = Player(test_render_group)

        actual.return_home()

        self.assertEqual(actual.rect.x, expected.rect.x)
        self.assertEqual(actual.rect.y, expected.rect.y)
        self.assertEqual(actual.index, expected.index)
        self.assertEqual(actual.direction, expected.direction)

        actual.farthest_distance = 265
        expected.score += 50 + 2 * test_timer

        actual.nest(test_timer, nest)

        self.assertEqual(actual.farthest_distance, expected.farthest_distance)
        self.assertEqual(actual.score, expected.score)
        self.assertTrue(actual.disabled_nests.has(nest))

        actual.win_game()
        expected.score += 2000

        self.assertEqual(actual.score, expected.score)

        actual.kill()
        expected.lives_left -= 1

        self.assertEqual(actual.lives_left, expected.lives_left)

    def test_nests_group(self):
        test_render_group = pygame.sprite.LayeredUpdates()
        test_player = Player(test_render_group)
        test_disabled_nests = DisabledNests()
        test_timer = 0

        self.assertFalse(DisabledNests.check_for_win(test_player))

        nest = FrogNest(1)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertFalse(DisabledNests.check_for_win(test_player))

        nest = FrogNest(2)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertFalse(DisabledNests.check_for_win(test_player))

        nest = FrogNest(3)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertFalse(DisabledNests.check_for_win(test_player))

        nest = FrogNest(4)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertFalse(DisabledNests.check_for_win(test_player))

        nest = FrogNest(5)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertTrue(DisabledNests.check_for_win(test_player))

        nest = FrogNest(1)
        nest.disable(test_render_group, test_disabled_nests, test_player)
        self.assertTrue(DisabledNests.check_for_win(test_player))

    def test_car_spawner(self):
        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_groups = [pygame.sprite.RenderUpdates(), DeathSprites()]
        test_win = pygame.Surface((820, 876))
        assert_groups = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                         pygame.sprite.Group(), pygame.sprite.Group()]

        # test that all lanes spawn properly
        obstacle_spawner.spawn_car_lanes(0, car_test_lanes[0], car_test_lanes[1], car_test_lanes[2], car_test_lanes[3],
                                         car_test_lanes[4], test_groups, test_win)

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

        test_groups[0].empty()
        test_groups[1].empty()

    def test_car_mover(self):

        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = [pygame.sprite.RenderUpdates()]
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
                                         car_test_lanes[4], test_render_group, test_win)

        for car_test_lanes, assert_group in zip(car_test_lanes, assert_groups):
            for i, j in zip(car_test_lanes.sprites(), assert_group.sprites()):
                self.assertEqual(i.rect.x, j.rect.x)
                self.assertEqual(i.rect.y, j.rect.y)
            assert_group.empty()
            car_test_lanes.empty()

        test_render_group[0].empty()

    def test_car_despawner(self):

        car_test_lanes = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(),
                          pygame.sprite.Group(), pygame.sprite.Group()]
        test_render_group = [pygame.sprite.RenderUpdates()]
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
                                         car_test_lanes[4], test_render_group, test_win)

        for lane in car_test_lanes:
            self.assertFalse(lane.has())

        test_render_group[0].empty()

    def test_move_player(self):
        """Test whether the movement system works as expected"""
        test_render_group = pygame.sprite.LayeredUpdates()
        test_player = Player(test_render_group)
        pygame.mixer.init()
        test_sound = pygame.mixer.Sound("../Assets/Sounds/hop.wav")
        up = 119  # 'w' key ascii
        left = 97  # 'a' key ascii
        right = 100  # 'd' key ascii
        down = 115  # 's' key ascii

        MOVEMENT_DISTANCE_X = AssetDictionary.get_asset("frog").get_width() + 4
        MOVEMENT_DISTANCE_Y = AssetDictionary.get_asset("frog").get_height() + 12

        # Test move up
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, up, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.y, 400 - MOVEMENT_DISTANCE_Y)

        # Test move left
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, left, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.x, 400 - MOVEMENT_DISTANCE_X)

        # Test move right
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, right, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.x, 400 + MOVEMENT_DISTANCE_X)

        # Test move down
        test_player.rect.x = 400
        test_player.rect.y = 400
        move_player(test_player, down, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.y, 400 + MOVEMENT_DISTANCE_Y)

        # Test move left if player is at left edge
        test_player.rect.x = 20
        test_player.rect.y = 400
        move_player(test_player, left, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.x, 20)

        # Test move right if player is at right edge
        test_player.rect.x = 750
        test_player.rect.y = 400
        move_player(test_player, right, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.x, 750)

        # Test move up if player is at top edge
        test_player.rect.x = 400
        test_player.rect.y = 20
        move_player(test_player, up, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.y, 20)

        # Test move down if player is at bottom edge
        test_player.rect.x = 800
        test_player.rect.y = 400
        move_player(test_player, down, MOVEMENT_DISTANCE_X, MOVEMENT_DISTANCE_Y, test_sound)
        self.assertEqual(test_player.rect.x, 800)

    def test_player_score(self):
        test_player = Player(pygame.sprite.LayeredUpdates())

        self.assertEqual(test_player.score, 0)

        test_player.set_score(0)
        self.assertEqual(test_player.score, 0.01)

        test_player.move("w")
        test_player.set_score(10)
        self.assertEqual(round(test_player.score, 2), 10.02)
        self.assertEqual(test_player.last_advancement, 10)

        test_player.move("d")
        test_player.set_score(11)
        self.assertEqual(round(test_player.score, 2), 10.03)
        self.assertEqual(test_player.last_advancement, 10)

        test_player.move("a")
        test_player.set_score(12)
        self.assertEqual(round(test_player.score, 2), 10.04)
        self.assertEqual(test_player.last_advancement, 10)

        test_player.move("s")
        test_player.set_score(13)
        self.assertEqual(round(test_player.score, 2), 10.05)
        self.assertEqual(test_player.last_advancement, 10)

        test_player.move("w")
        test_player.move("w")
        test_player.set_score(14)
        self.assertEqual(round(test_player.score, 2), 20.06)
        self.assertEqual(test_player.last_advancement, 14)

    def test_find_distance_to_sprite_ahead(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_net_group = pygame.sprite.Group()
        test_car = Player(pygame.sprite.LayeredUpdates())

        expected = test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car in front of the player
        test_car.rect.x = test_player.rect.x
        test_car.rect.y = test_player.rect.y - 50
        test_net_group.add(test_car)

        expected = test_player.rect.center[1] - test_car.rect.y
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x -= 10
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x += 20
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x += 1000
        expected = test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_car2 = Player(pygame.sprite.LayeredUpdates())
        test_net_group.add(test_car2)
        test_car.rect.y += 150
        test_car2.rect.x = test_player.rect.x
        test_car2.rect.y = test_player.rect.y - 50
        expected = test_player.rect.center[1] - test_car2.rect.y
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x = test_player.rect.x
        test_car.rect.y = 0
        actual = test_player.find_distance_to_sprite("ahead", test_net_group)
        self.assertEqual(expected, actual)


    def test_find_distance_to_sprite_behind(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_player.rect.y -= 500
        test_net_group = pygame.sprite.Group()
        test_car = Player(pygame.sprite.LayeredUpdates())

        expected = Window.HEIGHT - test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car behind the player
        test_car.rect.x = test_player.rect.x
        test_car.rect.y = test_player.rect.y + 50
        test_net_group.add(test_car)

        expected = test_car.rect.y - test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x -= 10
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x += 20
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x += 1000
        expected = Window.HEIGHT - test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y += 150
        test_car2 = Player(pygame.sprite.LayeredUpdates())
        test_net_group.add(test_car2)
        test_car2.rect.x = test_player.rect.x
        test_car2.rect.y = test_player.rect.y + 50
        expected = test_car2.rect.y - test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x = test_player.rect.x
        test_car.rect.y = Window.HEIGHT - test_car.rect.height
        expected = test_car2.rect.y - test_player.rect.center[1]
        actual = test_player.find_distance_to_sprite("down", test_net_group)
        self.assertEqual(expected, actual)


    def test_find_distance_to_left_sprite(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_net_group = pygame.sprite.Group()
        test_car = Player(pygame.sprite.LayeredUpdates())

        expected = test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car to the left side of the player
        test_car.rect.y = test_player.rect.y
        test_car.rect.x = test_player.rect.x - 50
        test_car.add(test_net_group)

        expected = test_player.rect.center[0] - (test_car.rect.x + test_car.rect.width)
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y += 10
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y -= 10
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y -= 1000
        expected = test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x += 150
        test_car2 = Player(pygame.sprite.LayeredUpdates())
        test_net_group.add(test_car2)
        test_car2.rect.y = test_player.rect.y
        test_car2.rect.x = test_player.rect.x - 50
        expected = test_player.rect.center[0] - (test_car2.rect.x + test_car.rect.width)
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y = test_player.rect.y
        test_car.rect.x = 0
        expected = test_player.rect.center[0] - (test_car2.rect.x + test_car.rect.width)
        actual = test_player.find_distance_to_sprite("left", test_net_group)
        self.assertEqual(expected, actual)

    def test_find_distance_to_right_sprite(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_net_group = pygame.sprite.Group()
        test_car = Player(pygame.sprite.LayeredUpdates())

        expected = Window.WIDTH - test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car to the right side of the player
        test_car.rect.y = test_player.rect.y
        test_car.rect.x = test_player.rect.x + 50
        test_car.add(test_net_group)

        expected = test_car.rect.x - test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y += 10
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y -= 10
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y -= 1000
        expected = Window.WIDTH - test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.x -= 150
        test_car2 = Player(pygame.sprite.LayeredUpdates())
        test_net_group.add(test_car2)
        test_car2.rect.y = test_player.rect.y
        test_car2.rect.x = test_player.rect.x + 50
        expected = test_car2.rect.x - test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

        test_car.rect.y = test_player.rect.y
        test_car.rect.x = Window.WIDTH
        expected = test_car2.rect.x - test_player.rect.center[0]
        actual = test_player.find_distance_to_sprite("right", test_net_group)
        self.assertEqual(expected, actual)

    def test_distance_in_lane_ahead(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_net_group = pygame.sprite.Group()
        test_carL = Player(pygame.sprite.LayeredUpdates())
        test_carR = Player(pygame.sprite.LayeredUpdates())

        expected = (test_player.rect.center[0], Window.WIDTH - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("ahead", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car to the lane ahead, left of the player
        test_carL.rect.y -= 64
        test_carL.rect.x = test_player.rect.x - 50
        test_carR.rect.y -= 64
        test_carR.rect.x = test_player.rect.x + 50

        test_net_group.add(test_carL, test_carR)
        expected = (test_player.rect.center[0] - (test_carL.rect.x + test_carL.rect.width),
                    test_carR.rect.x - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_carL2 = Player(pygame.sprite.LayeredUpdates())
        test_carR2 = Player(pygame.sprite.LayeredUpdates())
        test_carL2.rect.y -= 64
        test_carL2.rect.x = test_player.rect.x - 200
        test_carR2.rect.y -= 64
        test_carR2.rect.x = test_player.rect.x + 200
        test_net_group.add(test_carL2, test_carR2)
        expected = (test_player.rect.center[0] - (test_carL.rect.x + test_carL.rect.width),
                    test_carR.rect.x - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("ahead", test_net_group)
        self.assertEqual(expected, actual)

        test_carL.rect.y, test_carR.rect.y, test_carL2.rect.y, test_carR2.rect.y = 500, 500, 500, 500
        expected = (test_player.rect.center[0], Window.WIDTH - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("ahead", test_net_group)
        self.assertEqual(expected, actual)


    def test_distance_in_lane_behind(self):
        test_player = Player(pygame.sprite.LayeredUpdates())
        test_net_group = pygame.sprite.Group()
        test_carL = Player(pygame.sprite.LayeredUpdates())
        test_carR = Player(pygame.sprite.LayeredUpdates())

        expected = (test_player.rect.center[0], Window.WIDTH - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("down", test_net_group)
        self.assertEqual(expected, actual)

        # Move the test car to the lane ahead, left of the player
        test_carL.rect.y += 64
        test_carL.rect.x = test_player.rect.x - 50
        test_carR.rect.y += 64
        test_carR.rect.x = test_player.rect.x + 50

        test_net_group.add(test_carL, test_carR)
        expected = (test_player.rect.center[0] - (test_carL.rect.x + test_carL.rect.width),
                    test_carR.rect.x - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("down", test_net_group)
        self.assertEqual(expected, actual)

        test_carL2 = Player(pygame.sprite.LayeredUpdates())
        test_carR2 = Player(pygame.sprite.LayeredUpdates())
        test_carL2.rect.y += 64
        test_carL2.rect.x = test_player.rect.x - 200
        test_carR2.rect.y += 64
        test_carR2.rect.x = test_player.rect.x + 200
        test_net_group.add(test_carL2, test_carR2)
        expected = (test_player.rect.center[0] - (test_carL.rect.x + test_carL.rect.width),
                    test_carR.rect.x - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("down", test_net_group)
        self.assertEqual(expected, actual)

        test_carL.rect.y, test_carR.rect.y, test_carL2.rect.y, test_carR2.rect.y = 500, 500, 500, 500
        expected = (test_player.rect.center[0], Window.WIDTH - test_player.rect.center[0])
        actual = test_player.find_sprite_in_next_lane("down", test_net_group)
        self.assertEqual(expected, actual)
