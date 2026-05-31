import pygame
from .._net import Global

class Camera:
    def __init__(self, x=0, y=0, vx=0.0, vy=0.0, zoom=1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.zoom = zoom

        self.follow_target = None
        self.offset = None
        self.speed = 0.0


        if Global.cam is None:
            Global.cam = self

    def update(self):
        self.x+=self.vx*Global.dt
        self.y+=self.vy*Global.dt

        if self.follow_target is not None:
            self.x = (self.x+(self.follow_target.x+self.offset[0]-self.x)*self.speed)
            self.y = (self.y+(self.follow_target.y+self.offset[1]-self.y)*self.speed)

    def set_follow_target(self, target, speed=0.2):
        self.follow_target = target
        self.speed = speed
        self.offset = (self.x - target.x, self.y - target.y)

