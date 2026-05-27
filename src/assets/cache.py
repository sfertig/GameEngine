import pygame
from .._net import Global

class _Cache:
    def __init__(self):
        self.images: dict[str, pygame.surface.Surface] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def clear(self):
        self.images = {}
        self.fonts = {}

    def new_image(self, path, name, colorkey=None) -> bool:
        if name in self.images:
            return False
        self.images[name] = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            self.images[name].set_colorkey(colorkey)
        return True
    
    def get_image(self, name, copy=False) -> pygame.surface.Surface:
        if copy: return self.images[name].copy()
        else: return self.images[name]

Assets = _Cache()

