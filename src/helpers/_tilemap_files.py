import pygame
import json

from .._net import Global


def __saveTileMap_json__(path, data:dict[tuple[int, int ], tuple[int, int]], collisions:dict[tuple[int, int], int]):
    new_data = {}
    #covert data into json arrays
    for key, value in data.items():
        new_data[str(key)] = [value[0], value[1]]
    new_collisions = {}
    for key, value in collisions.items():
        new_collisions[str(key)] = [value[0], value[1]]
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

