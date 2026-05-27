import pygame
from src import Engine

pygame.init()

game = Engine(RESIZABLE=True)

while True:
    game.Tick()
