import pygame

from .math import Vector2

class Node:
    def __init__(self): 
        self.parent = None
        self.children = []
    def update(self, events, dt): pass
    def render(self, screen): pass
    def move(self, pos: Vector2): pass

class Node2D(Node):
    def __init__(self, pos, scale): 
        super().__init__()
        self.pos = pos
        self.scale = scale
    def move(self, pos: Vector2): 
        self.pos += pos
        for child in self.children: child.move(pos)

