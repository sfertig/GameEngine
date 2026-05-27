import pygame
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)
cam = Camera(vx=-1, vy=-2)
rect = Rect(0, 0, 100, 65, "red")

while True:
    game.Tick()
