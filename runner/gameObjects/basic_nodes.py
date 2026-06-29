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
    def __init__(self, x, y): 
        super().__init__()
        self.pos = Vector2(x, y)
        self.layer = 0
    def set_layer(self, layer):
        self.layer = layer
    def move(self, pos: Vector2): 
        for child in self.children: child.move(pos)

    def update(self, events, dt): pass

