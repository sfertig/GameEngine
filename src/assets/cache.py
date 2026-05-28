import pygame
from .._net import Global
from .animations import Animation
class _Cache:
    def __init__(self):
        self.images: dict[str, pygame.surface.Surface] = {}
        self.animations: dict[str, Animation] = {}
        self.tilesets: dict[str, dict[tuple[int, int], pygame.surface.Surface]] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    def clear_all(self, _confirm=False):
        if not _confirm: return
        self.images.clear()
        self.animations.clear()
        self.tilesets.clear()
        self.fonts.clear()

    #########################
    #CREATION
    #########################

    def new_image(self, path, name, colorkey=None, scale=1.0) -> bool:
        if name in self.images:
            return False
        self.images[name] = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            self.images[name].set_colorkey(colorkey)
        if scale != 1.0:
            self.images[name] = pygame.transform.scale(self.images[name], (int(self.images[name].get_width()*scale), int(self.images[name].get_height()*scale)))
        return True
    
    def new_animation(self, image, name, frames, width=16, height=16, loop=True, speed=0.3, layer=3, show=True) -> bool:
        if name in self.animations:
            return False
        self.animations[name] = Animation(name, image, frames, width, height, loop, speed, layer, show)
        return True
    
    def new_tileset(self, path, name, width=16, height=16, scale=1.0, colorkey=None) -> bool:
        image = pygame.image.load(path).convert_alpha()
        if colorkey is not None:
            image.set_colorkey(colorkey)
        if scale != 1.0:
            image = pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))
        self.tilesets[name] = load_tileset(image, width*scale, height*scale)
    
    ########################
    #REMOVING
    ########################

    def remove_image(self, name):
        if name in self.images:
            del self.images[name]

    def remove_animation(self, name):
        if name in self.animations:
            del self.animations[name]

    def remove_tileset(self, name):
        if name in self.tilesets:
            del self.tilesets[name]

    ########################
    #GETTERS
    ########################
    
    def get_image(self, name, copy=False) -> pygame.surface.Surface:
        if copy: return self.images[name].copy()
        else: return self.images[name]

    def get_animation(self, name) -> Animation:
        return self.animations[name]
    
    def get_tileset(self, name) -> pygame.surface.Surface:
        return self.tilesets[name]

Assets = _Cache()

def load_tileset(image, width, height):
    tileset = {}
    for y in range(int(image.get_height()//height)):
        for x in range(int(image.get_width()//width)):
            tileset[(x, y)] = image.subsurface(pygame.Rect(x*width, y*height, width, height))
    return tileset

