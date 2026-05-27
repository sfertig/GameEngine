import pygame
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
cam = Camera()
rect = Rect(0, 0, 100, 65, "red")
speed = 100

c = Circle(0, 0, 50, "blue", layer=7)

while True:
    game.Tick()

    rect.vx=0.0
    rect.vy=0.0
    if Keys.is_held(Keys.w): rect.vy=-speed
    if Keys.is_held(Keys.s): rect.vy=speed
    if Keys.is_held(Keys.a): rect.vx=-speed
    if Keys.is_held(Keys.d): rect.vx=speed

