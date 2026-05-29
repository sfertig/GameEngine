import pygame
from .._net import Global
from ..helpers.utils import change_layer
from .collisions import CollisionRect
class DynamicBody:
    def __init__(self, x, y, width, height, vx=0.0, vy=0.0, show=True, layer=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.show = show
        self.layer = layer

        self.collision = CollisionRect(x, y, width, height)
        self.collision.layers = [layer]

        Global.add_object(layer, self)

        self.shape = None
        self.image = None
        self.animation = None

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def update(self):

        #x movement
        self.x+=self.vx*Global.dt
        #if collisions, back up
        self.collision.x = self.x
        if self.collision.isColliding():
            self.x-=self.vx*Global.dt

        self.collision.x = self.x

        #y movement
        self.y+=self.vy*Global.dt
        #if collisions, back up
        self.collision.y = self.y
        if self.collision.isColliding():
            self.y-=self.vy*Global.dt

        self.collision.y = self.y

        #update any other positions now
        if self.shape is not None:
            self.shape.x = self.x
            self.shape.y = self.y

        if self.image is not None:
            self.image.x = self.x
            self.image.y = self.y

        if self.animation is not None:
            self.animation.x = self.x
            self.animation.y = self.y

