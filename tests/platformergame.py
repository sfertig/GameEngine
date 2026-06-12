import pygame
import os
from src.devPace import *

pygame.init()

game = Engine(title="Platformer Game", TARGET_FPS=60)
G = game._func_get_global_()

class titleScreen(Scene):
    def __init__(self):
        super().__init__()
    def on_start(self):
        game.bg = "blue"
        self.cam = Camera()

    def run(self):
        while True:
            game.Tick()

            if Keys.is_pressed(Keys.enter): game.change_scene("main")


class mainGame(Scene):
    def __init__(self):
        super().__init__()
        #load assets
        Assets.new_tileset("tests/assets/TileSet/PL #1 TileSet(Ground).png", "ground", scale=2.0)
        Assets.new_tileset("tests/assets/PL #3 Species(Grass & flowers).png", "props", scale=2.0, colorkey=(0, 0, 0))

    def on_start(self):
        game.bg = "black"
        self.cam = Camera()

        #player
        self.player = DynamicBody(200, 300, 32, 32, gravity=500.0)
        self.player.shape = Rect(0, 0, 32, 32, "green")
        #move cam to put player in center
        self.cam.x = self.player.x - game.screen.get_width()//2
        self.cam.y = self.player.y - game.screen.get_height()//2
        self.cam.set_follow_target(self.player, 1.0)

        self.playerMovement = FastMovement(self.player, 100.0, reset_y=False, move_y=False, jump=True, jumpKeys=[Keys.space, Keys.w, Keys.up], jumpForce=self.player.gravity//1.5)

        #tilemap
        self.map = Tilemap("ground", Assets.get_tileset("ground"), collisionLayers=game.all_colision_layers(), dataFile = "tests/game.json")
        self.map.manual_load_json("tests/game.json")

        self.props = Tilemap("props", Assets.get_tileset("props"), dataFile = "tests/props.json", layer=5)
        self.props.manual_load_json("tests/props.json")

        #goal
        self.goal = Rect(400, 200, 100, 5, "yellow", layer=0)


    def run(self):
        while True:
            game.Tick()            

            #creating the map
            if Keys.is_pressed(Keys.escape): self.props.activateEditor(exit_key=Keys.escape, _pin=(self.player.x, self.player.y))

            #game over (loss)
            if self.player.y >= 2000: game.reload_scene()
            #gen over (win)
            if self.player.y <= 0: game.change_scene("title")



#creating scenes in game and running
if __name__ == "__main__": 
    game.new_scene("main", mainGame())
    game.new_scene("title", titleScreen())

    game.change_scene("title")
