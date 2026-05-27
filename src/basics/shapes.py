import pygame
from .._net import Global
from ..physics.collisions import CollisionRect
from ..helpers.utils import change_layer

class _Shape:
    def __init__(self, x, y, vx, vy, show):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.show = show

        self.collision: CollisionRect = None

    def update(self):
        self.x+=self.vx*Global.dt
        self.y+=self.vy*Global.dt
        if self.collision is not None:
            self.collision.x = self.x
            self.collision.y = self.y

class Rect(_Shape):
    def __init__(self, x, y, width, height, color, _width=0, vx=0.0, vy=0.0, show=True, layer=3, enableCollision=False):
        super().__init__(x, y, vx, vy, show)
        self.layer = layer
        self.width=width
        self.height = height
        self.color = color
        self._width=_width
        Global.add_object(layer, self)
        if enableCollision:
            self.collision: CollisionRect = CollisionRect(x, y, width, height)

        print(Global.objects)

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def enableCollision(self):
        self.collision = CollisionRect(self.x, self.y, self.width, self.height)

    def render(self):
        if self.show:
            rect = self.rect()
            rect.x = self.x-Global.cam.x
            rect.y = self.y-Global.cam.y
            pygame.draw.rect(Global.screen, self.color, rect, self._width)

class Circle(_Shape):
    def __init__(self, x, y, radius, color, _width=0, vx=0.0, vy=0.0, show=True, layer=3, enableCollision=False):
        super().__init__(x, y, vx, vy, show)
        self.layer = layer
        self.r = radius
        self.color = color
        self._width=_width
        Global.add_object(layer, self)

        if enableCollision:
            self.collision = CollisionRect(x, y, radius*2, radius*2)

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def enableCollision(self):
        self.collision = CollisionRect(self.x, self.y, self.r*2, self.r*2)

    def render(self):
        if self.show:
            pygame.draw.circle(Global.screen, self.color, (self.x-Global.cam.x, self.y-Global.cam.y), self.r, self._width)

