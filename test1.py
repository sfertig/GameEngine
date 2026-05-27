import pygame
from src import *

pygame.init()

game = Engine(bg="green", RESIZABLE=True)

rect = Rect(0, 0, 100, 65, "red")

while True:
    game.Tick()
