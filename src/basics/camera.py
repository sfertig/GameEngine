import pygame
from .._net import Global

class Camera:
    def __init__(self, x=0, y=0, vx=0.0, vy=0.0, zoom=1.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.zoom = zoom

        Global.cam = self

    def update(self):
        self.x+=self.vx*Global.dt
        self.y+=self.vy*Global.dt

