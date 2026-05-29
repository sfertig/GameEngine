import pygame
import os
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
#game.create_aroundScreen_bounds()
G = game._func_get_global_()
cam = Camera()

Assets.new_image("tests/assets/test.png", "test", scale=2.0)
Assets.new_animation(Assets.get_image("test"), "test", [0, 2], 32, 32, loop=True, show=True, speed=0.4)

#load tileset into assets
Assets.new_tileset("tests/assets/levelTiles.png", "map1", scale=2.0)

rect = DynamicBody(0, 0, 32, 32)
rect.animation = Assets.get_animation("test")

map = Tilemap("map1", Assets.tilesets["map1"], layer=1, dataFile="test.json")
map.manual_load_json("test.json")

Rect(100, 100, 50, 60, "red", 5, enableCollision=True)
for i in G.collisions:
    print(i.layers)


while True:
    game.Tick()

    rect.vx=0.0
    rect.vy=0.0
    speed=100
    if Keys.is_held(Keys.shift): speed=200
    if Keys.is_held(Keys.w): rect.vy=-speed
    if Keys.is_held(Keys.s): rect.vy=speed
    if Keys.is_held(Keys.a): rect.vx=-speed
    if Keys.is_held(Keys.d): rect.vx=speed

    if Keys.is_pressed(Keys.escape): map.activateEditor()
    if Keys.is_pressed(Keys.p): map.manual_save_json("test.json")

