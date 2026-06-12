"""
Pygame Engine
"""


__version__ = "1.0.0"
__author__ = "Sam Fertig"

#____imports____
from .main import Engine, Scene
from .basics.camera import Camera
from .basics.input import Keys, FastMovement
from .basics.shapes import Rect, Circle
from .assets.cache import Assets
from .assets.images import Image
from .physics.dynamicBody import DynamicBody
from .physics.KinematicPlatform import KinematicPlatform
from .assets.tilemap import Tilemap, TILEMAP_COLLISION_GEN
from .assets.animations import AnimationManager
from .physics.StateManager import StateManager, AutoStateManager
from .helpers.timers import Timer

__all__ = [
    "Engine",
    "Scene",
    "Camera",
    "Rect",
    "Keys",
    "FastMovement",
    "Circle",
    "Assets",
    "Image",
    "DynamicBody",
    "KinematicPlatform",
    "Tilemap",
    "TILEMAP_COLLISION_GEN",
    "AnimationManager",
    "StateManager",
    "AutoStateManager",
    "Timer",
    ]