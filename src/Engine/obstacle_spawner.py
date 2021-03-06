import pygame
from Sprites.log import Log
from Sprites.car import Car
from Sprites.turtle import Turtle
from Sprites.turtle_animated import TurtleSinker
from Util.asset_dictionary import AssetDictionary


def sprite_despawner(sprite, win):
    x = sprite.rect.x
    y = sprite.rect.y

    if x + sprite.rect.width < 0 or x > win.get_width() + 1:
        sprite.kill()

    if y + sprite.rect.height < 0 or y > win.get_height() + 1:
        sprite.kill()


def spawn_water_lanes(framecount, lane1, lane2, lane3, lane4, lane5, render_group, asset_dict: AssetDictionary, win):
    """Handle spawning water platforms"""

    # Spawns turtles in lane 1 every 2 seconds, spawning a sinking turtle every 4th spawn
    if framecount % 60 == 0:
        if framecount % 180 == 0:
            TurtleSinker(asset_dict.get_asset("triple-turtle-sink"), framecount, 821, 372, 10).add(lane1, render_group)
        else:
            Turtle(asset_dict.get_asset("triple-turtle"), framecount, 821, 372).add(lane1, render_group)

    # Spawns logs in lane 2 every 8 seconds, skipping every 4th spawn
    if framecount == 0 or (framecount % 240 == 0 and framecount % 960 != 0):
        Log(asset_dict.get_asset("log-short"), -999, 308).add(lane2, render_group)

    # Spawns logs in lane 3 every 9 seconds
    if framecount % 270 == 0:
        Log(asset_dict.get_asset("log-long"), -999, 244).add(lane3, render_group)

    # Spawns turtles in lane 4 every 3 seconds, skipping every 5th spawn and sinking turtle every 6th
    if framecount % 90 == 0:
        if framecount % 540 == 0:
            TurtleSinker(asset_dict.get_asset("double-turtle-sink"), framecount, 821, 180).add(lane4, render_group)
        elif framecount % 450 != 0:
            Turtle(asset_dict.get_asset("double-turtle"), framecount, 821, 180).add(lane4, render_group)

    # Spawns logs in lane 5 every 5 seconds
    if framecount % 150 == 0:
        Log(asset_dict.get_asset("log-medium"), -999, 116).add(lane5, render_group)

    lane1_sprites = lane1.sprites()
    lane2_sprites = lane2.sprites()
    lane3_sprites = lane3.sprites()
    lane4_sprites = lane4.sprites()
    lane5_sprites = lane5.sprites()

    # Moves all entities in lane 1 at a constant speed and kill them if they have moved offscreen
    for sprite in lane1_sprites:
        sprite.rect.x -= 5
        sprite_despawner(sprite, win)

    # Moves all entities in lane 2 at a constant speed and kill them if they have moved offscreen
    for sprite in lane2_sprites:
        sprite.rect.x += 1
        sprite_despawner(sprite, win)

    # Moves all entities in lane 3 at a constant speed and kill them if they have moved offscreen
    for sprite in lane3_sprites:
        sprite.rect.x += 3
        sprite_despawner(sprite, win)

    # Moves all entities in lane 4 at a constant speed and kill them if they have moved offscreen
    for sprite in lane4_sprites:
        sprite.rect.x -= 3
        sprite_despawner(sprite, win)

    # Moves all entities in lane 5 at a constant speed and kill them if they have moved offscreen
    for sprite in lane5_sprites:
        sprite.rect.x += 2
        sprite_despawner(sprite, win)


def spawn_car_lanes(framecount, carlane1, carlane2, carlane3, carlane4, carlane5, render_group, kill_group,
                    asset_dict: AssetDictionary, win: pygame.surface.Surface):
    """Handle spawning car platforms"""
    # Spawns cars  in lane 1 every 8 seconds
    if framecount % 240 == 0:
        Car(asset_dict.get_asset("car1"), 800, 750, win).add(carlane1, render_group, kill_group)

    # Spawns cars in lane 2 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict.get_asset("car2"), 800, 700, win).add(carlane2, render_group, kill_group)

    # Spawns cars in lane 3 every 5 seconds
    if framecount % 150 == 0:
        Car(asset_dict.get_asset("car3"), 800, 630, win).add(carlane3, render_group, kill_group)

    # Spawns cars  in lane 4 every 8 seconds, skipping the 4th spawn
    if framecount == 0 or (framecount % 240 == 0 and framecount % 960 != 0):
        Car(asset_dict.get_asset("car4"), 800, 560, win).add(carlane4, render_group, kill_group)

    # Spawns cars in lane 5 every 9 seconds
    if framecount % 270 == 0:
        Car(asset_dict.get_asset("semi-truck"), 800, 500, win).add(carlane5, render_group, kill_group)

    carlane1_sprites = carlane1.sprites()
    carlane2_sprites = carlane2.sprites()
    carlane3_sprites = carlane3.sprites()
    carlane4_sprites = carlane4.sprites()
    carlane5_sprites = carlane5.sprites()

    # Moves all cars in lane 1 at a constant speed and kill if go off screen
    for sprite in carlane1_sprites:
        sprite.rect.x += -1.5
        sprite_despawner(sprite, win)

    # Moves all cars in lane 2 at a constant speed and kill if go off screen
    for sprite in carlane2_sprites:
        sprite.rect.x += -3.25
        sprite_despawner(sprite, win)

    # Moves all cars in lane 3 at a constant speed and kill if go off screen
    for sprite in carlane3_sprites:
        sprite.rect.x += -2.25
        sprite_despawner(sprite, win)

    # Moves all cars in lane 4 at a constant speed and kill if go off screen
    for sprite in carlane4_sprites:
        sprite.rect.x += -1.5
        sprite_despawner(sprite, win)

    # Moves all cars in lane 5 at a constant speed and kill if go off screen
    for sprite in carlane5_sprites:
        sprite.rect.x += -3.25
        sprite_despawner(sprite, win)
