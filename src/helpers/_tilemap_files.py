import pygame
import json
import os

from .._net import Global
from ..physics.collisions import CollisionRect


def __saveTileMap_json__(path, data:dict[tuple[int, int ], tuple[int, int]], collisions:dict[tuple[int, int], int]):
    new_data = {}
    #covert data into json arrays
    for key, value in data.items():
        new_data[str(key)] = [value[0], value[1]]
    new_collisions = {}
    for key, value in collisions.items():
        new_collisions[str(key)] = value
    #save file
    with open(path, "w") as f:
        json.dump({"map": new_data, "coll": new_collisions}, f)

def __loadTileMap_json__(path):
    with open(path, "r") as f:
        i = json.load(f)
        data = i["map"]
        coll = i["coll"]
    info = {}
    for key, value in data.items():
        info[extract_tuple_from_str(key)] = tuple(value)
    collisions = {}
    for key, value in coll.items():
        collisions[extract_tuple_from_str(key)] = value
    return info, collisions

def extract_tuple_from_str(str):
    return tuple(float(x) for x in str[1:-1].split(","))


def gen_collision_shapes(self, COL_FULL, COL_HALF_TOP, COL_HALF_BOTTOM, COL_HALF_LEFT, COL_HALF_RIGHT, SEARCH_TIME):
    [t.Del() for t in self.collisions]
    self.collisions.clear()
    
    # Separate tiles into shapes
    full = []
    half_top = []
    half_bottom = []
    half_left = []
    half_right = []
    
    for key, value in self.tiles.items():
        if value not in self.collDef: 
            continue
        # CORRECTION: Appending 'key' (grid pos) instead of 'value' (tile type)
        if self.collDef[value] == COL_FULL: full.append(key)
        elif self.collDef[value] == COL_HALF_TOP: half_top.append(key)
        elif self.collDef[value] == COL_HALF_BOTTOM: half_bottom.append(key)
        elif self.collDef[value] == COL_HALF_LEFT: half_left.append(key)
        elif self.collDef[value] == COL_HALF_RIGHT: half_right.append(key)


    # Gen collision shapes
    _tiles = []
    used = []
    rows: list[CollisionRect] = _gen_tiles_left_right([], used, full, self, SEARCH_TIME, CollisionRect(0, 0, self.width, self.height, self.collisionLayers))
    #join rows to form rects
    for shape in rows:
        if shape in used: continue
        #else this is current shape to attempt and match
        #used.append(shape)
        _tiles.append(shape)
        for i in range(SEARCH_TIME):
            for other_shape in rows:
                if other_shape in used: continue
                #elif above, and width is the same, and x is the same
                if other_shape.y == shape.y-other_shape.height and other_shape.width == shape.width and other_shape.x == shape.x:
                    shape.y -= other_shape.height
                    shape.height += other_shape.height
                    other_shape.Del()
                    used.append(other_shape)
                #elif below, and width is the same, and x is the same
                if other_shape.y == shape.y+shape.height and other_shape.width == shape.width and other_shape.x == shape.x:
                    shape.height += other_shape.height
                    other_shape.Del()
                    used.append(other_shape)
        
    #half top tiles
    _tiles = _gen_tiles_left_right(_tiles, used, half_top, self, SEARCH_TIME, CollisionRect(0, 0, self.width, self.height//2, self.collisionLayers))
    #half bottom tiles
    _tiles = _gen_tiles_left_right(_tiles, used, half_bottom, self, SEARCH_TIME, CollisionRect(0, self.height//2, self.width, self.height//2, self.collisionLayers))
    #half left tiles
    _tiles = _gen_tiles_top_bottom(_tiles, used, half_left, self, SEARCH_TIME, CollisionRect(0, 0, self.width//2, self.height, self.collisionLayers))
    #half right tiles
    _tiles = _gen_tiles_top_bottom(_tiles, used, half_right, self, SEARCH_TIME, CollisionRect(self.width//2, 0, self.width//2, self.height, self.collisionLayers))
        
    # CORRECTION: Make sure generated rectangles are actually added to your active collisions list
    for i in _tiles:
        self.collisions.append(i)
    #print(len(self.collisions))
    #print(len(Global.collisions))

def _gen_tiles_left_right(_tiles: list[CollisionRect], used: list, _pos_list: list[tuple], self, SEARCH_TIME: int, shape: CollisionRect):
    used.clear()
    for pos in _pos_list:
        if pos in used: continue
        col = shape.copy()
        #move shape to correct position
        col.x += pos[0]*self.width
        col.y += pos[1]*self.height
        _tiles.append(col)
        used.append(pos)
        #run search through tiles
        for i in range(SEARCH_TIME):
            for tile in _pos_list:
                if tile in used: continue
                #else check left then right
                if tile[0] == (col.x//self.width)-1 and tile[1] == pos[1]:
                    col.x -= self.width
                    col.width += self.width
                    used.append(tile)
                elif tile[0] == (col.x+col.width)//self.width and tile[1] == pos[1]:
                    col.width += self.width
                    used.append(tile)
                #else leave it be
    #clear collisions shape used as template
    shape.Del()
    return _tiles

def _gen_tiles_top_bottom(_tiles: list[CollisionRect], used: list, _pos_list: list[tuple], self, SEARCH_TIME: int, shape: CollisionRect):
    used.clear()
    for pos in _pos_list:
        if pos in used: continue
        col = CollisionRect.copy(shape)
        #move shape to correct position
        col.x += pos[0]*self.width
        col.y += pos[1]*self.height
        _tiles.append(col)
        used.append(pos)
        #run search through tiles
        for i in range(SEARCH_TIME):
            for tile in _pos_list:
                if tile in used: continue
                #else check left then right
                if tile[1] == (col.y//self.height)-1 and tile[0] == pos[0]:
                    col.y -= self.height
                    col.height += self.height
                    used.append(tile)
                elif tile[1] == (col.y+col.height)//self.height and tile[0] == pos[0]:
                    col.height += self.height
                    used.append(tile)
                #else leave it be
    #clear collisions shape used as template
    shape.Del()
    return _tiles


