import pygame

from .math import Vector2

class Node:
    def __init__(self): 
        self.parent = None
        self.children = []
    def update(self, events, dt): pass
    def render(self, screen): pass
    def move(self, pos: Vector2): pass
    def set_layer(self, layer): pass

class Node2D(Node):
    def __init__(self, x, y, width, height, scale_x, scale_y): 
        super().__init__()
        self.pos = Vector2(x, y)
        self.size = Vector2(width, height)
        self.scale = Vector2(scale_x, scale_y)
        self.layer = 0
        print(x, y)
    def set_layer(self, layer):
        self.layer = layer
    def move(self, pos: Vector2): 
        self.pos += pos
        for child in self.children: child.move(pos)

    def update(self, events, dt): print(self.parent)

