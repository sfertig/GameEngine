import pygame

from .._net import Global


class CollisionRect:
    def __init__(self, x, y, width, height, layers=[]):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.layers = layers
        Global.collisions.append(self)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def isColliding(self):
        for obj in Global.collisions:
            if obj == self: continue
            for layer in self.layers:
                if layer in obj.layers:
                    if obj.rect().colliderect(self.rect()):
                        return True

        return False
    
    def render(self):
        rect = self.rect()
        rect.x = self.x-Global.cam.x
        rect.y = self.y-Global.cam.y
        pygame.draw.rect(Global.screen, "yellow", rect)
