import pygame
import os
from src import *

pygame.init()

game = Engine(bg="green", TARGET_FPS=60, EXPERIMENTAL_RESIZABLE=True)
#game.create_aroundScreen_bounds()
G = game._func_get_global_()
Assets.new_image("tests/assets/test.png", "test", scale=2.0)

Assets.new_animation(Assets.get_image("test"), "test", [0, 2], 32, 32, loop=True, show=True, speed=0.4)

#load tileset into assets
Assets.new_tileset("tests/assets/levelTiles.png", "map1", scale=2.0)


class testScene(Scene):
    def __init__(self):
        super().__init__()
    def on_start(self):
        self.cam = Camera()

        self.rect = DynamicBody(game.screen_dim[0]/2, game.screen_dim[1]/2, 32, 32)
        self.rect.animation = Assets.get_animation("test")
        self.cam.set_follow_target(self.rect)

        self.map = Tilemap("map1", Assets.tilesets["map1"], layer=1, dataFile="test.json", collisionLayers=game.all_colision_layers())
        self.map.manual_load_json("test.json")

    def run(self):
        while True:
            game.Tick()
            game.change_title(str(int(game.get_current_fps())))

            self.rect.vx=0.0
            self.rect.vy=0.0
            speed=100
            if Keys.is_held(Keys.shift): speed=200
            if Keys.is_held(Keys.w): self.rect.vy=-speed
            if Keys.is_held(Keys.s): self.rect.vy=speed
            if Keys.is_held(Keys.a): self.rect.vx=-speed
            if Keys.is_held(Keys.d): self.rect.vx=speed

            if Keys.is_pressed(Keys.escape): self.map.activateEditor()

game.new_scene("test", testScene())
game.change_scene("test")