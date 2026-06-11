import pygame
import os
from .._net import Global
from ..helpers.utils import change_layer
from ..basics.camera import Camera
from ..basics.input import Keys
from ..physics.collisions import CollisionRect

from ..helpers._tilemapEditor import _TileMapEditor
from ..helpers._tilemap_files import __saveTileMap_json__, __loadTileMap_json__, gen_collision_shapes

#tilemap collision types
COL_FULL = 1
COL_HALF_TOP = 2
COL_HALF_BOTTOM = 3
COL_HALF_LEFT = 4
COL_HALF_RIGHT = 5

#collision gen vars
TILEMAP_COLLISION_GEN = 25
SEARCH_TIME = TILEMAP_COLLISION_GEN

class Tilemap:
    def __init__(self, name, tileset, show=True, layer=3, dataFile=None, collisionLayers=None):
        self.name = name
        self.tileset: dict[tuple[int, int], pygame.surface.Surface] = tileset
        self.width = tileset[0, 0].get_width()
        self.height = tileset[0, 0].get_height()
        self.show = show
        self.layer = layer

        if collisionLayers is not None: self.collisionLayers = collisionLayers
        else: self.collisionLayers = [layer]

        self.dataFile = dataFile

        self.tiles: dict[tuple[int, int ], tuple[int, int]] = {}
        self.collisions = []
        self.collDef: dict[tuple[int, int], int] = {}

        Global.add_object(layer, self)

        #fallback for hardcoded tilemaps (no loading from file)
        self.__gen_self_collision_shapes()

    def change_layer(self, new_layer):
        change_layer(self, new_layer, self.layer)
        self.layer = new_layer

    
    def __gen_self_collision_shapes(self):
        gen_collision_shapes(self, COL_FULL, COL_HALF_TOP, COL_HALF_BOTTOM, COL_HALF_LEFT, COL_HALF_RIGHT, SEARCH_TIME)

    def manual_save_json(self, path=None):
        if path and self.dataFile == None: return
        if path is None: path = self.dataFile
        __saveTileMap_json__(path, self.tiles, self.collDef)
    def manual_load_json(self, path):
        if path and self.dataFile == None: return
        if path is None: path = self.dataFile
        self.tiles, self.collDef = __loadTileMap_json__(path)
        self.__gen_self_collision_shapes()

    def activateEditor(self, exit_key=Keys.escape, _pin=(0, 0)):
        x, y = pygame.display.get_window_position()
        _TileMapEditor(x, y, Global.display.get_width(), Global.display.get_height(), self, exit_key, _pin).run()
        self.manual_save_json()
        self.__gen_self_collision_shapes()

    def render(self):
        if not self.show: return
        for pos, tile in self.tiles.items():
            tx = pos[0] * self.width - Global.cam.x
            ty = pos[1] * self.height - Global.cam.y
            if tx > -self.width and tx < Global.screen.get_width()+self.width and ty > -self.height and ty < Global.screen.get_height()+self.height:
                image = self.tileset[tile]
                Global.screen.blit(image, (tx, ty))

def tile_beside(pos, _pos):
    if _pos[0] == pos[0]+1: return True
    elif _pos[0] == pos[0]-1: return True
    return False
def tile_above(pos, _pos):
    if _pos[1] == pos[1]+1: return True
    elif _pos[1] == pos[1]-1: return True
    return False
