import pygame
import json

from .._net import Global


def __saveTileMap_json__(path, data:dict[tuple[int, int ], tuple[int, int]]):
    new_data = {}
    #covert data into json arrays
    for key, value in data.items():
        new_data[str(key)] = [value[0], value[1]]
    #save file
    with open(path, "w") as f:
        json.dump(new_data, f)