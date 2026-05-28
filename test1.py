import pygame
import os
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
game.create_aroundScreen_bounds()
G = game._func_get_global_()
cam = Camera()

Assets.new_image("tests/assets/test.png", "test", scale=3.0)
Assets.new_animation(Assets.get_image("test"), "test", [0, 2], 16, 16, loop=True, show=True, speed=0.4)

rect = DynamicBody(0, 0, Assets.get_image("test").get_width(), Assets.get_image("test").get_height())
rect.animation = Assets.get_animation("test")


while True:
    game.Tick()

    rect.vx=0.0
    rect.vy=0.0
    speed=100
    if Keys.is_held(Keys.shift): speed=200
    #print(rect.x, rect.y, rect.animation.x, rect.animation.y, rect.animation.time, rect.animation.frame)
    if Keys.is_held(Keys.w): rect.vy=-speed
    if Keys.is_held(Keys.s): rect.vy=speed
    if Keys.is_held(Keys.a): rect.vx=-speed
    if Keys.is_held(Keys.d): rect.vx=speed

