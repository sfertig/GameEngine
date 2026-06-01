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
    os.system("cls")
    print("Generating collision shapes...")
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
    rows: list[CollisionRect] = []
    for pos in full:
        if pos in used: continue
        #else creat new collision and run search
        col = CollisionRect(pos[0]*self.width, pos[1]*self.height, self.width, self.height, self.collisionLayers)
        #run search through tiles
        for i in range(SEARCH_TIME):
            for tile in full:
                if tile in used: continue
                #else check if it can be added to col shape
                #if to the left
                if tile[0] == (col.x//self.width)-1 and tile[1] == pos[1]:
                    col.x -= self.width
                    col.width += self.width
                    used.append(tile)
                #else check if it is to the right
                if tile[0] == (col.x+col.width)//self.width and tile[1] == pos[1]:
                    col.width += self.width
                    used.append(tile)
                #else leave it be
        #apend col to rows
        rows.append(col)
    used.clear()
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
    
        
    # CORRECTION: Make sure generated rectangles are actually added to your active collisions list
    for i in _tiles:
        self.collisions.append(i)
    print(len(self.collisions))
    print(len(Global.collisions))

