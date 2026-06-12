import pygame
import os
from src import *

pygame.init()

game = Engine()
G = game._func_get_global_()

class mainGame(Scene):
    def __init__(self):
        super().__init__()
        #load assets
        Assets.new_tileset("tests/assets/TileSet/PL #1 TileSet(Ground).png", "ground", scale=2.0)

    def on_start(self):
        self.cam = Camera()

        #player
        self.player = DynamicBody(200, 300, 32, 32, gravity=500.0)
        self.player.shape = Rect(0, 0, 32, 32, "green")
        self.cam.x -= self.player.x//2
        self.cam.y -= self.player.y//2
        self.cam.set_follow_target(self.player)

        self.playerSpeed = 200
        self.playerSprintSpeed = 1.5

        #tilemap
        self.map = Tilemap("ground", Assets.get_tileset("ground"), collisionLayers=game.all_colision_layers(), dataFile = "tests/game.json")
        self.map.manual_load_json("tests/game.json")

        #goal
        self.goal = Rect(400, 200, 100, 5, "yellow", layer=0)


    def run(self):
        while True:
            game.Tick()

            #player movement
            speed = self.playerSpeed
            self.player.vx = 0.0
            if Keys.is_held(Keys.shift): speed = self.playerSpeed * self.playerSprintSpeed
            if Keys.is_held(Keys.a): self.player.vx = -speed
            if Keys.is_held(Keys.d): self.player.vx = speed
            if Keys.is_pressed([Keys.w, Keys.space]) and self.player.is_on_floor: self.player.vy = -self.player.gravity//2

            #creating the map
            if Keys.is_pressed(Keys.escape): self.map.activateEditor(exit_key=Keys.escape, _pin=(self.player.x, self.player.y))

            #game over (loss)
            if self.player.y >= 2000: game.reload_scene()

    def on_end(self):
        print("end")


#creating scenes in game and running
if __name__ == "__main__": 
    game.new_scene("main", mainGame())

    game.change_scene("main")
