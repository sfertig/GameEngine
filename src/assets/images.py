import pygame

from .._net import Global
from .cache import Assets
from ..utils import change_layer



class Image:
    def __init__(self, image, colorkey=None, x=0, y=0, scale=1.0, show=True, layer=3):
        self.image = image
        if scale != 1.0:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*scale), int(self.image.get_height()*scale)))
        self.colorkey = colorkey
        self.x = x
        self.y = y
        self.show = show
        self.layer = layer

        Global.add_object(layer, self)

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def render(self, x=None, y=None):
        if self.show:
            x, y = x or self.x, y or self.y
            Global.screen.blit(self.image, (x-Global.cam.x, y-Global.cam.y))

