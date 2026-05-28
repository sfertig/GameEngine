import pygame
from .._net import Global
from .images import Image
#from .cache import Assets
from ..helpers.utils import change_layer
from ..physics.collisions import CollisionRect

def splitImage(image, width, height, frames):
    images = []
    #split image into frames
    for y in range(image.get_height()//height):
        for x in range(image.get_width()//width):
            images.append(image.subsurface(pygame.Rect(x*width, y*height, width, height)))
    new_images = []
    #extract each frame

    #if all
    if frames == "_ALL": return images
    #else return range
    for i in range(frames[0], frames[1]+1):
        new_images.append(images[i])
    return new_images

class Animation:
    def __init__(self, name, image, frames, width=16, height=16, x=0, y=0, loop=True, speed=0.3, layer=3, show=True, enableCollision=False):
        self.name = name
        self.frames = splitImage(image, width, height, frames)
        self.frame = 0
        self.loop = loop
        self.speed = speed
        self.layer = layer
        self.show = show
        self.time = 0.0
        self.x = x
        self.y = y

        Global.add_object(layer, self)

        self.collision = None
        if enableCollision:
            self.collision = CollisionRect(x, y, width, height)
            self.collision.layers = [layer]

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    def update(self):
        if self.collision is not None:
            self.collision.x = self.x
            self.collision.y = self.y
        #update using Global.dt
        self.time+=Global.dt
        if self.time >= self.speed:
            self.time = 0.0
            self.frame+=1
            if self.frame > len(self.frames)-1:
                if self.loop:
                    self.frame = 0

    def enableCollision(self):
        self.collision = CollisionRect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def get_frame(self):
        return self.frames[self.frame]

    def render(self):
        if self.show:
            Global.screen.blit(self.frames[self.frame], (self.x-Global.cam.x, self.y-Global.cam.y))
