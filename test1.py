import pygame
import os
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
game.create_aroundScreen_bounds()
cam = Camera()

Assets.new_image("tests/assets/test.png", "test")

rect = DynamicBody(0, 0, Assets.get_image("test").get_width(), Assets.get_image("test").get_height())
rect.shape = Rect(0, 0, rect.width, rect.height, "red")


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

    if Keys.is_pressed(Keys.space): os.system("cls")

