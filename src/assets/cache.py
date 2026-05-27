import pygame
from .._net import Global

class Cache:
    def __init__(self):
        self.images: dict[str, pygame.surface.Surface] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def clear(self):
        self.images = {}
        self.fonts = {}

