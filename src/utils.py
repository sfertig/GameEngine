import pygame
from ._net import Global

def change_layer(self, new_layer, layer):
        Global.remove_object(layer, self)
        Global.add_object(new_layer, self)

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)