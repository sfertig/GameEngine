import pygame
from .._net import Global

class _Shape:
    def __init__(self, x, y, vx, vy, show):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.show = show

    def update(self):
        self.x+=self.vx*Global.dt
        self.y+=self.vy*Global.dt

class Rect(_Shape):
    def __init__(self, x, y, width, height, color, _width=0, vx=0.0, vy=0.0, show=True, layer=3):
        super().__init__(x, y, vx, vy, show)
        self.layer = layer
        self.width=width
        self.height = height
        self.color = color
        self._width=_width
        Global.add_object(layer, self)

        print(Global.objects)

    def change_layer(self, new_layer):
        Global.remove_object(self.layer, self)
        Global.add_object(new_layer, self)
        self.layer = new_layer

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self):
        if self.show:
            rect = self.rect()
            rect.x = self.x-Global.cam.x
            rect.y = self.y-Global.cam.y
            pygame.draw.rect(Global.screen, self.color, rect, self._width)

class Circle(_Shape):
    def __init__(self, x, y, radius, color, _width=0, vx=0.0, vy=0.0, show=True, layer=3):
        super().__init__(x, y, vx, vy, show)
        self.layer = layer
        self.r = radius
        self.color = color
        self._width=_width
        Global.add_object(layer, self)

    def change_layer(self, new_layer):
        Global.remove_object(self.layer, self)
        Global.add_object(new_layer, self)
        self.layer = new_layer

    def render(self):
        if self.show:
            pygame.draw.circle(Global.screen, self.color, (self.x-Global.cam.x, self.y-Global.cam.y), self.r, self._width)

