import pygame
from .._net import Global
from ..helpers.utils import change_layer
from .collisions import CollisionRect
class DynamicBody:
    def __init__(self, x, y, width, height, vx=0.0, vy=0.0, max_vx=None, max_vy=None, show=True, layer=3, gravity=0.0, smartCollisions=True, smartCollisionDist=1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.max_vx = max_vx
        self.max_vy = max_vy
        self.width = width
        self.height = height
        self.show = show
        self.layer = layer
        self.gravity = gravity

        self.collision = CollisionRect(x, y, width, height)
        self.collision.layers = [layer]

        Global.add_object(layer, self)

        self.shape = None
        self.image = None
        self.animation = None
        self.animationManager = None
        self.area2D = None

        #collision checks
        self.smartCollisions = smartCollisions
        self.smartCollisionDist = smartCollisionDist

        self.is_on_floor = False
        self.is_on_ceiling = False
        self.is_on_left = False
        self.is_on_right = False
        self.is_on_wall = False


    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer


    def update(self):  

        #collision checks
        self.is_on_floor = False
        self.is_on_ceiling = False
        self.is_on_left = False
        self.is_on_right = False
        self.is_on_wall = False

        #clamps
        if self.max_vx != None:
            if self.vx > self.max_vx:
                self.vx = self.max_vx
            elif self.vx < -self.max_vx:
                self.vx = -self.max_vx

        if self.max_vy != None:
            if self.vy > self.max_vy:
                self.vy = self.max_vy
            elif self.vy < -self.max_vy:
                self.vy = -self.max_vy

        #x movement
        self.x+=self.vx*Global.dt
        #if collisions, back up
        self.collision.x = self.x
        if self.collision.isColliding():
            self.x-=self.vx*Global.dt
            #colisions info
            self.is_on_wall = True
            if self.vx > 0.0:
                self.is_on_right = True
            elif self.vx < 0.0:
                self.is_on_left = True
            self.vx = 0

        if self.smartCollisions:
            if not self.is_on_left:
                self.collision.x = self.x - self.smartCollisionDist
                if self.collision.isColliding():
                    self.is_on_left = True
                    self.vx = 0.0
                self.collision.x = self.x

            if not self.is_on_right:
                self.collision.x = self.x + self.smartCollisionDist
                if self.collision.isColliding():
                    self.is_on_right = True
                    self.vx = 0.0
                self.collision.x = self.x

        #y movement
        self.y += self.vy*Global.dt
        #if collisions, back up
        self.collision.y = self.y
        if self.collision.isColliding():
            self.y-=self.vy*Global.dt

            #collision info
            if self.vy > 0.0:
                self.is_on_floor = True
            if self.vy < 0.0:
                self.is_on_ceiling = True

            self.vy = 0

        if self.smartCollisions:
            if not self.is_on_floor:
                self.collision.y = self.y + self.smartCollisionDist
                if self.collision.isColliding():
                    self.is_on_floor = True
                    self.vy = 0.0
                self.collision.y = self.y

            if not self.is_on_ceiling:
                self.collision.y = self.y - self.smartCollisionDist
                if self.collision.isColliding():
                    self.is_on_ceiling = True
                    self.vy = 0.0
                self.collision.y = self.y

        #gravity
        if not self.is_on_floor:
            self.vy += self.gravity*Global.dt


        self.collision.x = self.x
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

        if self.animationManager is not None:
            self.animationManager.x = self.x
            self.animationManager.y = self.y
        if self.area2D is not None:
            self.area2D.x = self.x
            self.area2D.y = self.y

