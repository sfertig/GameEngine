import pygame
import os
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
cam = Camera()
rect = Rect(0, 0, 100, 65, "red", enableCollision=True)
rect.collision.layers = [1]

speed = 100

#load assets
Assets.new_image("tests/assets/test.png", "test")

i = Image(Assets.get_image("test"), layer=1, enableCollision=True)
i.collision.layers = [1]


while True:
    game.Tick()

    if i.collision.isColliding(): print("colliding")

    rect.vx=0.0
    rect.vy=0.0
    if Keys.is_held(Keys.w): rect.vy=-speed
    if Keys.is_held(Keys.s): rect.vy=speed
    if Keys.is_held(Keys.a): rect.vx=-speed
    if Keys.is_held(Keys.d): rect.vx=speed

    if Keys.is_pressed(Keys.space): os.system("cls")

