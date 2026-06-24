import pygame

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ZERO = Vector2(0, 0)
        self.UP = Vector2(0, -1)
        self.DOWN = Vector2(0, 1)
        self.LEFT = Vector2(-1, 0)
        self.RIGHT = Vector2(1, 0)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
    
    def __mul__(self, other):
        if isinstance(other, Vector2): 
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if isinstance(other, Vector2): 
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)
        
    def copy(self):
        return Vector2(self.x, self.y)
