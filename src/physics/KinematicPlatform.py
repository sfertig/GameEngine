import pygame

from .._net import Global


import pygame
from .._net import Global
from ..helpers.utils import change_layer
from .collisions import CollisionRect
class KinematicPlatform:
    def __init__(self, x, y, width, height, speed, show=True, layer=3, waypoints=[], loop=True, snapDist = 5):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.width = width
        self.height = height
        self.show = show
        self.layer = layer

        self.waypoints = waypoints
        self.currentWaypoint = 0
        self.speed = speed
        self.loop = loop
        self.snapDist = snapDist

        self.collision = CollisionRect(x, y, width, height)
        self.collision.layers = [layer]

        Global.add_object(layer, self)

        self.shape = None
        self.image = None
        self.animation = None
        self.animationManager = None

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def update(self):
        self.vx = 0.0
        self.vy = 0.0
        #move toward current waypoint
        if self.currentWaypoint < len(self.waypoints):
            if self.x > self.waypoints[self.currentWaypoint][0]:
                self.vx = -self.speed
            elif self.x < self.waypoints[self.currentWaypoint][0]:
                self.vx = self.speed
            if self.y > self.waypoints[self.currentWaypoint][1]:
                self.vy = -self.speed
            elif self.y < self.waypoints[self.currentWaypoint][1]:
                self.vy = self.speed

            #if at waypoint,or snapdist, move to next waypoint
            if abs(self.x - self.waypoints[self.currentWaypoint][0]) < self.snapDist and abs(self.y - self.waypoints[self.currentWaypoint][1]) < self.snapDist:
                self.currentWaypoint+=1
                if self.currentWaypoint >= len(self.waypoints):
                    if self.loop:
                        self.currentWaypoint = 0

            

        #x movement
        self.x+=self.vx*Global.dt
        self.collision.x = self.x
        self.y+=self.vy*Global.dt
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


