import pygame
from Sprites.log import Log
from Sprites.car import Car
from Sprites.turtle import Turtle
from Util.asset_dictionary import AssetDictionary


def spawn_water_lanes(framecount, lane1, lane2, lane3, lane4, lane5, render_group, asset_dict: AssetDictionary, width, win):
    """Handle spawning water platforms"""

    # Spawns turtles in lane 1 every 2 seconds
    if framecount % 60 == 0:
        Turtle(asset_dict.get_asset("turtle-1"), 821, 372, win).add(lane1, render_group)

    # Spawns logs in lane 2 every 8 seconds, skipping every 4th spawn
    if framecount == 0 or (framecount % 240 == 0 and framecount % 960 != 0):
        Log(asset_dict.get_asset("log-short"), -999, 308).add(lane2, render_group)

    # Spawns logs in lane 3 every 9 seconds
    if framecount % 270 == 0:
        Log(asset_dict.get_asset("log-long"), -999, 244).add(lane3, render_group)

    # Spawns turtles in lane 4 every 3 seconds
    if framecount % 90 == 0:
        Turtle(asset_dict.get_asset("double-turtle-1"), 821, 180, win).add(lane4, render_group)

    # Spawns logs in lane 5 every 5 seconds
    if framecount % 150 == 0:
        Log(asset_dict.get_asset("log-short"), -999, 116).add(lane5, render_group)

    lane1_sprites = lane1.sprites()
    lane2_sprites = lane2.sprites()
    lane3_sprites = lane3.sprites()
    lane4_sprites = lane4.sprites()
    lane5_sprites = lane5.sprites()

    # Moves all entities in lane 1 at a constant speed and kill them if they have moved offscreen
    for sprite in lane1_sprites:
        sprite.rect.x -= 5
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all entities in lane 2 at a constant speed and kill them if they have moved offscreen
    for sprite in lane2_sprites:
        sprite.rect.x += 1
        if sprite.rect.x > width + 1:
            sprite.kill()

    # Moves all entities in lane 3 at a constant speed and kill them if they have moved offscreen
    for sprite in lane3_sprites:
        sprite.rect.x += 3
        if sprite.rect.x > width + 1:
            sprite.kill()

    # Moves all entities in lane 4 at a constant speed and kill them if they have moved offscreen
    for sprite in lane4_sprites:
        sprite.rect.x -= 3
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all entities in lane 5 at a constant speed and kill them if they have moved offscreen
    for sprite in lane5_sprites:
        sprite.rect.x += 2
        if sprite.rect.x > width + 1:
            sprite.kill()


def spawn_car_lanes(framecount, carlane1, carlane2, carlane3, carlane4, carlane5, render_group, kill_group,
                    asset_dict: AssetDictionary, win: pygame.surface.Surface):
    """Handle spawning car platforms"""
    # Spawns cars  in lane 1 every 8 seconds
    if framecount % 240 == 0:
        Car(asset_dict.get_asset("car1"), 0, 750, win).add(carlane1, render_group, kill_group)

    # Spawns cars in lane 2 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict.get_asset("car2"), 0, 700, win).add(carlane2, render_group, kill_group)

    # Spawns cars in lane 3 every 5 seconds
    if framecount % 150 == 0:
        Car(asset_dict.get_asset("car3"), 0, 630, win).add(carlane3, render_group, kill_group)

    # Spawns cars  in lane 4 every 8 seconds
    if framecount % 240 == 0:
        Car(asset_dict.get_asset("car4"), 0, 560, win).add(carlane4, render_group, kill_group)

    # Spawns cars in lane 5 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict.get_asset("semi-truck"), 0, 500, win).add(carlane5, render_group, kill_group)

    carlane1_sprites = carlane1.sprites()
    carlane2_sprites = carlane2.sprites()
    carlane3_sprites = carlane3.sprites()
    carlane4_sprites = carlane4.sprites()
    carlane5_sprites = carlane5.sprites()

    # Moves all cars in lane 1 at a constant speed and kill if go off screen
    for sprite in carlane1_sprites:
        sprite.rect.x += -1
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all cars in lane 2 at a constant speed and kill if go off screen
    for sprite in carlane2_sprites:
        sprite.rect.x += -3
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all cars in lane 3 at a constant speed and kill if go off screen
    for sprite in carlane3_sprites:
        sprite.rect.x += -2
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all cars in lane 4 at a constant speed and kill if go off screen
    for sprite in carlane4_sprites:
        sprite.rect.x += -1
        if sprite.rect.x + sprite.image.get_width() < 0:
            sprite.kill()

    # Moves all cars in lane 5 at a constant speed and kill if go off screen
    for sprite in carlane5_sprites:
        sprite.rect.x += -3
        if sprite.rect.x > win.get_width() + 1:
            sprite.kill()