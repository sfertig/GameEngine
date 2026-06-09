"""
Pygame Engine
"""


__version__ = "0.0.1"
__author__ = "Sam Fertig"

#____imports____
from .main import Engine, Scene
from .basics.camera import Camera
from .basics.input import Keys
from .basics.shapes import Rect, Circle
from .assets.cache import Assets
from .assets.images import Image
from .physics.dynamicBody import DynamicBody
from .assets.tilemap import Tilemap, TILEMAP_COLLISION_GEN
from .assets.animations import AnimationManager

__all__ = [
    "Engine",
    "Scene",
    "Camera",
    "Rect",
    "Keys",
    "Circle",
    "Assets",
    "Image",
    "DynamicBody",
    "Tilemap",
    "TILEMAP_COLLISION_GEN",
    "AnimationManager"
    ]